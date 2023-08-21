from __future__ import annotations
import os
from config.config_provider import ConfigProvider
from jinja2 import Environment, FileSystemLoader, select_autoescape
from data_extraction.data_extraction_service import DataExtractionService
from services.storage_service import StorageService
from sql.connection_factory import DatabaseConnectionFactory
import sys
import os.path


class DataExtractionProvider:

    @staticmethod
    def provide() -> DataExtractionService:
        config = ConfigProvider.provide()
        bundle_dir = getattr(
            sys, '_MEIPASS', "")

        dataExtractionService = DataExtractionService(
            Environment(
                loader=FileSystemLoader(
                    os.path.abspath(
                        os.path.join(
                            bundle_dir,
                            "templates"))),
                autoescape=select_autoescape(),
            ),
            StorageService().set_driver(
                config('DEFAULT_STORAGE_DRIVER')
            )
            .create_session()
            .create_client(),
            DatabaseConnectionFactory()
        )

        return dataExtractionService
