"""Default configuration for the application."""

# Database configuration
DATABASE = {
    "name": "cc.sqlite3",
    "pragmas": {"journal_mode": "wal", "cache_size": -1024 * 64},  # 64MB
}

# Flask configuration
DEBUG = True
TESTING = False
SECRET_KEY = "dev"  # Change this in production!

# Logging configuration
LOG_LEVEL = "INFO"  # Can be: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE_LEVEL = "INFO"
LOG_CONSOLE_LEVEL = "INFO"
