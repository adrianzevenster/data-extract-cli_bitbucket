from typing import TypedDict
from enum import Enum

"""
Typings useful for autocompletion
"""


class ExtractRun(TypedDict):
    tenant: str
    datasets: list
    id: str
    created_at: str
    status: str  # replace with an enum asap
    message: str
    sql: str
    sql_filters: dict
    current_data_uri: str
    dataset_urls: list
    extracted_by: str
    keep_local_data: bool
    total_rows: int


class ExtractStatus(str, Enum):
    STATUS_CREATED = 'CREATED'
    STATUS_EXTRACTING = 'EXTRACTING'
    STATUS_SUCCESS = 'SUCCESS'
    STATUS_ERROR = 'ERROR'


class ExtractConstants:
    DATETIME_FORMAT = "%Y:%m:%d %H:%M:%S"
    TYPE_LENDING_ADVANCES = 'lending_advances'
    TYPE_LENDING_PAYMENTS = 'lending_payments'
    TYPE_PROFILER_RECHARGES = 'profiler_recharges'
    SUPPORTED_TYPES = (TYPE_LENDING_ADVANCES,
                       TYPE_LENDING_PAYMENTS, TYPE_PROFILER_RECHARGES)
