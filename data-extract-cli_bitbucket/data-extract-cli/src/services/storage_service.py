import boto3
from config.config_provider import ConfigProvider

"""
This Service serves as an abstraction of any storage service we need to use.
For example if one tenant insists on on-prem disk, we don't need to change
the code too much, we donly need to user another driver.
"""


class StorageService:

    def __init__(self):
        self.config = ConfigProvider.provide()

    def set_driver(self, driver):
        self.driver = driver

        return self

    def create_session(self):
        if (self.driver == 's3'):
            self.session = boto3.Session(
                profile_name=self.config('AWS_PROFILE')
            )

        return self

    def create_client(self):
        if (self.driver == 's3'):
            self.client = self.session.client('s3')

        return self

    def get_client(self):
        return self.client or None
