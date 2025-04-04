"""Default configuration for the application."""

# Database configuration
DATABASE = {
    "name": "cc.sqlite3",
    "pragmas": {"journal_mode": "wal", "cache_size": -1024 * 64},  # 64MB
}

# Flask configuration
DEBUG = True
