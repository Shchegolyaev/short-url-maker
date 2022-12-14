import os
from logging import config as logging_config

from pydantic import BaseSettings, PostgresDsn

from core.logger import LOGGING

PROJECT_NAME = os.getenv("PROJECT_NAME", "ShortUrlMaker")
PROJECT_HOST = os.getenv("PROJECT_HOST", "0.0.0.0")
PROJECT_PORT = os.getenv("PROJECT_PORT", "8001")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logging_config.dictConfig(LOGGING)


class AppSettings(BaseSettings):
    app_title: str = "ShortUrlMaker"
    database_dsn: PostgresDsn

    class Config:
        env_file = ".env"


app_settings = AppSettings()
