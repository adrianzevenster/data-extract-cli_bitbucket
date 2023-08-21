
from datetime import datetime
from decouple import Config
from config.config_provider import ConfigProvider
from data_extraction.types import ExtractRun, ExtractConstants
import sys
import os


class TenantService:

    tenant_name: str
    config: Config

    def __init__(self, tenant_name):
        self.tenant_name = tenant_name
        self.config = ConfigProvider.provide()

    def get_storage_bucket_name(self) -> str:
        return self.config(f"{self.tenant_name}_STORAGE_BUCKET")

    def get_storage_extract_path(self, extract: ExtractRun) -> str:
        date = datetime.strptime(
            extract["created_at"], ExtractConstants.DATETIME_FORMAT
        )
        year = date.year
        month = date.month
        day = date.day

        return f"{self.config('APP_ENV')}/Data/Original/{year}/{month}-{day}/{extract['id']}"

    def get_storage_run_path(self, extract: ExtractRun) -> str:
        bundle_dir = getattr(
            sys, '_MEIPASS', "")

        return os.path.join(bundle_dir, "storage", "runs",
                            extract['id'])
