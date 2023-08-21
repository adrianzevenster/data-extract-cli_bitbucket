from behave.model import Scenario
import os
import boto3


def after_scenario(context, scenario: Scenario):
    if scenario.name == "A Successfull Data Extract":
        # remove the test-extract-request.json input file
        os.remove(context.input_json_path)


def before_all(context):
    context.awsSession = awsSession = boto3.Session(
        profile_name='elucidate'
    )
    os.environ.putenv('APP_ENV', 'testing')
