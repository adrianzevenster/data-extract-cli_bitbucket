from config.config_provider import ConfigProvider

config = ConfigProvider.provide()


class connections:
    MTC = {
        "engine": "mysql",
        "driver": "mysql",
        "database": config("MTC_LENDING_DB"),
        "host": config("MTC_HOST"),
        "port": config("MTC_PORT"),
        "username": config("MTC_USER"),
        "password": config("MTC_PW"),
    }
    TMCEL = {
        "engine": "mysql",
        "driver": "mysql",
        "database": config("TMCEL_LENDING_DB"),
        "host": config("TMCEL_HOST"),
        "port": config("TMCEL_PORT"),
        "username": config("TMCEL_USER"),
        "password": config("TMCEL_PW"),
    }
    DIGICELL = {
        "engine": "mysql",
        "driver": "mysql",
        "database": config("DIGICELL_LENDING_DB"),
        "host": config("DIGICELL_HOST"),
        "port": config("DIGICELL_PORT"),
        "username": config("DIGICELL_USER"),
        "password": config("DIGICELL_PW"),
    }
    DIGIBELIZE = {
        "engine": "mysql",
        "driver": "mysql",
        "database": config("DIGIBELIZE_LENDING_DB"),
        "host": config("DIGIBELIZE_HOST"),
        "port": config("DIGIBELIZE_PORT"),
        "username": config("DIGIBELIZE_USER"),
        "password": config("DIGIBELIZE_PW"),
    }
