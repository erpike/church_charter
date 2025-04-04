"""Production configuration."""

import os

from config.base import BaseConfig


class ProductionConfig(BaseConfig):
    DEBUG = False

    # Production-specific database settings
    DATABASE = {
        **BaseConfig.DATABASE,
        "name": os.environ.get("DB_NAME", "cc.sqlite3"),
    }

    # Production logging - less verbose, more focused on errors
    LOG_LEVEL = "INFO"
    LOG_FILE_LEVEL = "WARNING"
    LOG_CONSOLE_LEVEL = "ERROR"

    # Use environment variable for secret key in production
    SECRET_KEY = os.environ.get("SECRET_KEY", BaseConfig.SECRET_KEY)
