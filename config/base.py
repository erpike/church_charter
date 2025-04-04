"""Base configuration for the application."""

import os


class BaseConfig:
    # Database configuration
    DATABASE = {
        "name": "cc.sqlite3",
        "pragmas": {"journal_mode": "wal", "cache_size": -1024 * 64},  # 64MB
    }

    # Flask configuration
    TESTING = False
    SECRET_KEY = "dev"  # Change this in production!

    # Logging configuration
    LOG_LEVEL = "INFO"
    LOG_FILE_LEVEL = "INFO"
    LOG_CONSOLE_LEVEL = "INFO"

    # Admin credentials
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "password")
