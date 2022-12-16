import os
from logging import config as logging_config

from pydantic import BaseSettings, PostgresDsn

from core.logger import LOGGING

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logging_config.dictConfig(LOGGING)


class AppSettings(BaseSettings):
    app_title: str = "ShortUrlMaker"
    database_dsn: PostgresDsn
    project_host: str = "0.0.0.0"
    project_port: int = 8000

    class Config:
        env_file = ".env"


app_settings = AppSettings()
