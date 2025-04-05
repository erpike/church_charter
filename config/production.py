"""Production configuration."""

from config.base import BaseConfig


class ProductionConfig(BaseConfig):
    DEBUG = False

    # Production-specific settings
    SECRET_KEY = "your-secure-production-secret-key"  # Change this!

    # Admin credentials - should be overridden by environment variables
    ADMIN_USERNAME = "admin"  # Default, should be overridden
    ADMIN_PASSWORD = "change_this_password"  # Default, should be overridden

    # Production database settings
    DATABASE = {
        **BaseConfig.DATABASE,
        "name": "cc.sqlite3",
    }

    # Production logging
    LOG_LEVEL = "WARNING"
    LOG_FILE_LEVEL = "WARNING"
    LOG_CONSOLE_LEVEL = "ERROR"
