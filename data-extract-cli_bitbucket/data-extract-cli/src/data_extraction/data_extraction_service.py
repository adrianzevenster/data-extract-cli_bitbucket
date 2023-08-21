from __future__ import annotations
import logging
import json
import csv
import pandas as pd
from sql.connection_factory import DatabaseConnectionFactory
from data_extraction.dto import CleanupExtractDto
from data_extraction.types import ExtractRun, ExtractConstants, ExtractStatus
from tenants.tenant_service import TenantService
import os
import re
import getpass
import threading
import nanoid
from datetime import datetime
from smart_open import open
from services.storage_service import StorageService
from jinja2 import Environment, FileSystemLoader, select_autoescape
from cli.progress_updater import ProgressUpdater


class DataExtractionService:

    sql_builder: Environment
    chunksize: int
    current_extract: ExtractRun
    database_connection_factory: DatabaseConnectionFactory
    storage_service: StorageService
    progress_updater: ProgressUpdater

    def __init__(self, sql_builder, storage_service, database_factory):
        self.sql_builder = sql_builder
        self.chunksize = 1000  # default
        self.current_extract: ExtractRun = {
            "tenant": "",
            "datasets": [],
            "id": "",
            "created_at": "",
            "status": ExtractStatus.STATUS_CREATED,
            "message": "",
            "sql": "",
            "sql_filters": {},
            "current_data_uri": "",
            "dataset_urls": [],
            "extracted_by": getpass.getuser(),
            "total_rows": 0
        }
        self.database_connection_factory = database_factory
        self.storage_service = storage_service

    def read_extract_request(self, file_uri) -> dict:
        logging.info(
            f'Building the extract request input from json file: \n{file_uri}')
        return json.load(open(file_uri))

    def connect_to_sql(self):
        # in the case of Oracle we might have to connect to a specific database here
        self.sql_connection = self.database_connection_factory.build(
            self.current_extract['tenant']
        )

    def generate_query_from_sql_template(self, templateName, params) -> str:
        sql_string = self.sql_builder.get_template(
            templateName).render(params)
        logging.debug(f"SQL string from template: {sql_string}")

        return sql_string

    def save_extract_run_audit(self) -> DataExtractionService:
        # appData = os.getenv('APPDATA') # once the app is properly set up we will rather
        # want it to put it's data into the proper OS folder.
        if (self.current_extract['id']):
            path = os.path.join(self.tenant_service.get_storage_run_path(self.current_extract),
                                f"extract-run-audit.json")

            with open(path, 'w') as run_audit_stream:
                json.dump(self.current_extract, run_audit_stream)
        else:
            logging.warning(
                'Did not save the extract run audit, no id exists for current run.')

        return self

    def upload_extract_run_audit(self) -> None:
        if (self.current_extract['id']):
            path = os.path.join(self.tenant_service.get_storage_run_path(self.current_extract),
                                f"extract-run-audit.json")

            with open(path, 'r') as run_audit_stream:
                storage_extract_path = f"{self.tenant_service.get_storage_bucket_name()}/{self.tenant_service.get_storage_extract_path(self.current_extract)}"
                with open(
                        f"s3://{storage_extract_path}/extract-run-audit.json",
                        'w',
                        transport_params={
                            'client': self.storage_service.get_client()},
                        encoding='utf-8') as s3_stream:
                    s3_stream.write(run_audit_stream.read())
        else:
            logging.warning(
                'Did not upload the extract run audit, no id exists for current run.')

    def stream_data_from_sql_to_s3(self, query, params, extract_id, dataset) -> DataExtractionService:
        self.current_extract['current_data_uri'] = os.path.join(
            self.tenant_service.get_storage_run_path(self.current_extract),
            f"{dataset}.csv")

        with open(self.current_extract['current_data_uri'], 'a+') as csv_stream:
            write_header = True
            logging.info('Extracting chunks and saving local data.')
            for chunk_dataframe in pd.read_sql(
                    sql=query,
                    params=params,
                    con=self.sql_connection,
                    chunksize=self.chunksize):
                chunk_dataframe.to_csv(
                    csv_stream,
                    header=write_header,
                    index=False,
                    quoting=csv.QUOTE_NONNUMERIC
                )
                write_header = False
                self.current_extract['total_rows'] += self.chunksize
                # remember that any logging statement in this loop
                # will interfere with update outputs
                if (self.progress_updater):
                    self.progress_updater.update()

            if (self.progress_updater):
                self.progress_updater.update(
                    f"\nTotal Rows Processed: {self.current_extract['total_rows']}")

            # restart the CSV stream
            csv_stream.seek(0)
            # upload the data file to S3
            storage_extract_path = f"{self.tenant_service.get_storage_bucket_name()}/{self.tenant_service.get_storage_extract_path(self.current_extract)}"
            with open(
                f"s3://{storage_extract_path}/{dataset}.csv.gz",
                'wb',
                transport_params={'client': self.storage_service.get_client()},
                    encoding='utf-8') as s3_stream:
                logging.info(
                    'Compressing and uploading data to cloud storage.')
                s3_stream.write(csv_stream.read())
                # add the dataset's url to the run audit
                self.current_extract['dataset_urls'].append(
                    f"s3://{storage_extract_path}/{dataset}.csv.gz")

        return self

    def validate_input(self, json_input) -> None:
        if (bool(json_input['telco_name']) == False):
            raise Exception(
                "Empty `telco_name` in json input - please set it before running the extract.")
        if (bool(json_input['filters']) == False):
            raise Exception(
                "Empty `filters` in json input - please set them before running the extract.")
        if (bool(json_input['datasets']) == False):
            raise Exception(
                "Empty `datasets` array in json input - please set them before running the extract.")
        if (bool(json_input['sql_template_directory']) == True
                and not os.path.exists(os.path.abspath(json_input['sql_template_directory']))):
            raise Exception(
                "The `sql_template_directory` specified doesn't exist.")

    def set_progress_updater(self, progress_updater: ProgressUpdater) -> DataExtractionService:
        self.progress_updater = progress_updater

        return self

    def prepare_extract(self, input_json_path, chunksize, extract_id='') -> DataExtractionService:
        logging.info('Preparing extract')
        self.chunksize = chunksize
        # read the json input file and validate it
        json_input = self.read_extract_request(input_json_path)
        self.validate_input(json_input)
        # set the current extract details
        self.current_extract['id'] = extract_id or nanoid.generate(
            'abcdefghij0123456789', 6)
        self.current_extract['created_at'] = datetime.now().strftime(
            ExtractConstants.DATETIME_FORMAT
        )
        self.current_extract['tenant'] = json_input['telco_name']
        self.current_extract['keep_local_data'] = json_input['keep_local_data'] or False
        self.current_extract['datasets'] = json_input['datasets']
        self.current_extract['sql_filters'] = json_input['filters']
        # if there are tierids, cast them to an array for proper handling
        #   for ease of use it is entered as '1,2,3' for e.g.
        if (bool(self.current_extract['sql_filters']['tier_ids']) == True):
            self.current_extract['sql_filters']['tier_ids'] = list(
                map(int, self.current_extract['sql_filters']['tier_ids'].split(',')))
        # after we have the telco/tenant, instantiate the tenant service
        self.tenant_service = TenantService(self.current_extract['tenant'])
        # create the local directory for this extract run
        os.makedirs(self.tenant_service.get_storage_run_path(
            self.current_extract))
        # save the local data
        self.save_extract_run_audit()
        # connect the sql
        self.connect_to_sql()
        # if the user wanted their own custom template directory,
        # change the jinja template directory
        if (bool(json_input['sql_template_directory']) == True):
            self.sql_builder = Environment(
                loader=FileSystemLoader(
                    os.path.abspath(json_input['sql_template_directory'])
                ),
                autoescape=select_autoescape(),
            )

        return self

    def run_extract(self) -> bool:
        logging.info(
            f"Running extract. Your run ID is {self.current_extract['id']}")
        try:
            self.current_extract['status'] = ExtractStatus.STATUS_EXTRACTING

            sql_engine = self.database_connection_factory.connection_config['engine']

            # loop through all the datasets requested to ETL
            #   @todo - dispatch each one to it's own Thread
            for extract_type in self.current_extract['datasets']:
                # the datasets have a sql ending to point them to specific files
                #   we strip the sql ending so that we can use the type for other useful things
                extract_type = re.sub('\.sql$', '', extract_type)

                if (extract_type in ExtractConstants.SUPPORTED_TYPES):
                    logging.info(f"Attempting extract of {extract_type}.")
                    self.current_extract['sql'] = self.generate_query_from_sql_template(
                        f"{sql_engine}/{extract_type}.sql",
                        self.current_extract['sql_filters']
                    )
                    self.save_extract_run_audit()
                    self.stream_data_from_sql_to_s3(
                        self.current_extract['sql'],
                        self.current_extract['sql_filters'],
                        self.current_extract['id'],
                        extract_type
                    )
                else:
                    logging.warning(
                        f"Invalid extract dataset type specified `{extract_type}`")

            self.current_extract['status'] = ExtractStatus.STATUS_SUCCESS
            self.progress_updater.success('Extract is complete.')
            logging.info('Extract is complete.')

            return True
        except Exception as err:
            self.current_extract['status'] = ExtractStatus.STATUS_ERROR
            self.current_extract['message'] = str(err)
            self.progress_updater.error(str(err))
            raise err
        finally:
            # Using threads, we might want the program to be able to run other tasks while the delete is happening
            cleanup_dto: CleanupExtractDto = {
                "current_data_uri": self.current_extract['current_data_uri'],
                "keep_local_data": self.current_extract['keep_local_data'],
                "sql_connection": self.sql_connection,
                "storage_client": self.storage_service.get_client()
            }
            delete_thread = threading.Thread(
                target=clean_up,
                args=(cleanup_dto,),
                name=f"Delete CSV Data Run {self.current_extract['id']}")
            delete_thread.start()

            self.save_extract_run_audit()

            # If the extract is successfull, we upload the run audit json
            if (self.current_extract['status'] == ExtractStatus.STATUS_SUCCESS):
                logging.info(
                    'Uploading the audit info for the extract run to the cloud.')
                self.upload_extract_run_audit()


def clean_up(dto: CleanupExtractDto):
    logging.info('Running extract clean up.')
    # The CSV file could end up being huge, so we might have to remove it.
    if (bool(dto['keep_local_data']) == False):
        if (dto.get('current_data_uri') != None and
            dto.get('current_data_uri') != "" and
                os.path.exists(dto.get('current_data_uri'))):
            os.remove(dto['current_data_uri'])

    # close the SQL connection, hanging connections are very bad
    if (dto.get('sql_connection') != None and dto['sql_connection']):
        dto['sql_connection'].invalidate()

    # same for hanging connections but storage
    if (bool(dto.get('storage_client')) == True):
        dto['storage_client'].close()

    logging.info('Extract is cleaned up.')
