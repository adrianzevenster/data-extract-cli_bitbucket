from behave import given, when, then, step
import json
import subprocess
import nanoid
from datetime import datetime


@given('a valid extract-request.json input file')
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
        "keep_local_data": False,
        "sql_template_directory": "",
        "filters": {
            "loan_start_date": "2022-07-30 23:30:00",
            "loan_end_date": "2022-07-30 23:59:59",
            "historical_start_date": "2021-12-01",
            "historical_end_date": "2022-07-31",
            "tier_ids": "1,2,3",
            "msisdn_constraint": "264%"
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


@when('the `extract` CLI verb is called for run_extract')
def step_impl(context):
    input_json_path = context.input_json_path

    p = subprocess.Popen(
        f".venv/bin/python src/main.py --quiet 1 extract --input-json-path {input_json_path} --id {context.extract_id}", stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE
    )
    output, error = p.communicate()

    assert "error" not in str(error).lower(
    ) and "error" not in str(output).lower()


@then('I see a valid CSV data file on S3')
def step_impl(context):
    awsClient = context.awsSession.client('s3')
    # this path logic needs to be the same as the TenantServices'
    path = get_csv_path(context)
    response_code = 200

    try:
        awsClient.head_object(Bucket='mtc-av', Key=path)
    except Exception as err:
        response_code = int(err.response['Error']['Code'])

    assert response_code >= 200 and response_code < 300


def get_csv_path(context):
    date = context.created_at
    year = date.year
    month = date.month
    day = date.day

    return f"testing/Data/Original/{year}/{month}-{day}/{context.extract_id}/lending_advances.csv.gz"
