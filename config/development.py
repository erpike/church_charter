"""Development configuration."""

from config.base import BaseConfig


class DevelopmentConfig(BaseConfig):
    DEBUG = True

    # Development-specific database settings
    DATABASE = {
        **BaseConfig.DATABASE,
        "name": "cc.sqlite3",
    }

    # Development logging - more verbose
    LOG_LEVEL = "DEBUG"
    LOG_FILE_LEVEL = "DEBUG"
    LOG_CONSOLE_LEVEL = "INFO"
