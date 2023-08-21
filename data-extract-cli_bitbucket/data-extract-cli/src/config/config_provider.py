import sys
from decouple import Config, RepositoryEnv
import os


class ConfigProvider:

    @staticmethod
    def provide() -> Config:
        bundle_dir = getattr(
            sys, '_MEIPASS', "src")
        env_file_uri = os.path.join(bundle_dir, '.env')

        if os.path.exists(env_file_uri) == False:
            raise Exception(
                f"Please create file and configure environment variables at {env_file_uri}")

        return Config(RepositoryEnv(env_file_uri))
