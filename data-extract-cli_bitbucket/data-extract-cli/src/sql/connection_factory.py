import logging
from sqlalchemy import create_engine, engine
from config.database.database_config import connections


class DatabaseConnectionFactory:
    CONNECTION_TIMEOUT = 3600  # seconds

    def __init__(self):
        self.connection_config = {}

    def build(self, telco_name, database_name='') -> engine.Connection:
        self.connection_config = getattr(connections, telco_name)
        driver = self.connection_config['driver']
        username = self.connection_config['username']
        password = self.connection_config['password']
        host = self.connection_config['host']
        port = self.connection_config['port']
        database = database_name or self.connection_config['database']

        logging.info(
            f"Building SQL connection for {telco_name} - {database}")

        engine_string = f"{driver}://{username}:{password}@{host}:{port}/{database}"

        engine = create_engine(
            engine_string, pool_recycle=self.CONNECTION_TIMEOUT)
        logging.info(
            f"Attempting SQL connection to {telco_name} - {database}")
        con = engine.connect().execution_options(stream_results=True)
        logging.info(
            f"SQL Connection successfull for {telco_name} - {database}")

        return (con)
