import logging

from peewee import Proxy, SqliteDatabase
from peewee_migrate import Router

logger = logging.getLogger(__name__)


# Create a proxy database that will be configured later
db = Proxy()


def init_db(config=None):
    """Initialize database and run migrations."""
    if config is None:
        # Default configuration if none provided
        config = {
            "name": "cc.sqlite3",
            "pragmas": {"journal_mode": "wal", "cache_size": -1024 * 64},  # 64MB
        }

    logger.info(f"Connecting to database: {config['name']}")
    database = SqliteDatabase(
        config["name"],
        pragmas=config["pragmas"],
        autoconnect=False,
    )

    # Configure the proxy database
    db.initialize(database)

    with db:
        logger.info("Running database migrations...")
        router = Router(db, migrate_dir="storages/migrations")
        router.run()
        logger.info("Database migrations completed successfully")
