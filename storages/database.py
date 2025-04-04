from peewee import SqliteDatabase
from peewee_migrate import Router

db = SqliteDatabase(
    "cc.sqlite3",
    pragmas={
        'journal_mode': 'wal',
        'cache_size': -1024 * 64  # 64MB
    },
    autoconnect=False,
)

def init_db():
    """Initialize database and run migrations."""
    with db:
        router = Router(db, migrate_dir='storages/migrations')
        router.run()
