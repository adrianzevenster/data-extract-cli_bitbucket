from behave import given, when, then, step
import json
import subprocess
import nanoid
from datetime import datetime
from pandas import read_csv


@given('a extract-request.json input file requesting a full extract')
def step_impl(context):
    # create a valid json input file to extract small amount (30min) of data
    # from MTC tenant
    extract_request = {
        "telco_name": "MTC",
        "datasets": [
            "lending_advances.sql",
            "lending_payments.sql",
            "profiler_recharges.sql"
        ],
        "keep_local_data": True,  # keep the local CSV so we can test the contract
        "sql_template_directory": "",
        "filters": {
            "loan_start_date": "2022-07-30 23:30:00",
            "loan_end_date": "2022-07-30 23:59:59",
            "historical_start_date": "2021-12-01",
            "historical_end_date": "2022-07-31",
            "tier_ids": "",
            "msisdn_constraint": ""
        }
    }
    with open('./test-extract-request.json', 'w') as extract_request_stream:
        json.dump(extract_request, extract_request_stream)

    context.input_json_path = './test-extract-request.json'

    created_at = datetime.now()
    extract_id = nanoid.generate(
        'abcdefghij0123456789', 6)

    context.created_at = created_at
    context.extract_id = extract_id

    pass


@when('the `extract` CLI verb is called for data_contracts')
def step_impl(context):
    input_json_path = context.input_json_path

    p = subprocess.Popen(
        f".venv/bin/python src/main.py --quiet 1 extract --input-json-path {input_json_path} --id {context.extract_id}", stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE
    )
    output, error = p.communicate()

    assert "error" not in str(error).lower(
    ) and "error" not in str(output).lower()


@then('the CSV data conforms to the {dataset} contract')
def step_impl(context, dataset: str):
    # load the local CSV file here with pandas
    data_frame = read_csv(get_csv_path(context, dataset))

    # make sure the columns are what we expect for this dataset
    assert set(get_data_contract(dataset)[
               'columns']).issubset(data_frame.columns)


def get_csv_path(context, dataset) -> str:
    return f"storage/runs/{context.extract_id}/{dataset}.csv"


def get_data_contract(dataset) -> dict:
    return json.load(open(f"tests/data_contracts/{dataset}.json"))
