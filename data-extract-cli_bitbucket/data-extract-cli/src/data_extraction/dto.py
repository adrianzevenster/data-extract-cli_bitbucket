from typing import TypedDict
from sqlalchemy import engine
from boto3 import client

"""Typed Data Transfer Objects (DTO)

Use this file for creating useful statically-typed parameters to functions
"""


class CleanupExtractDto(TypedDict):
    data_file_uri: str
    sql_connection: engine.Connection
    storage_client: client
    keep_local_data: bool
