import logging

from peewee import SqliteDatabase
from peewee_migrate import Router

db = None
logger = logging.getLogger(__name__)


def init_db(config=None):
    """Initialize database and run migrations."""
    global db

    if db is not None:
        return

    if config is None:
        # Default configuration if none provided
        config = {
            "name": "cc.sqlite3",
            "pragmas": {"journal_mode": "wal", "cache_size": -1024 * 64},  # 64MB
        }

    logger.info(f"Connecting to database: {config['name']}")
    db = SqliteDatabase(
        config["name"],
        pragmas=config["pragmas"],
        autoconnect=False,
    )

    with db:
        logger.info("Running database migrations...")
        router = Router(db, migrate_dir="storages/migrations")
        router.run()
        logger.info("Database migrations completed successfully")
