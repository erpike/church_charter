from peewee import SqliteDatabase
from peewee_migrate import Router

db = None

def init_db(config=None):
    """Initialize database and run migrations."""
    global db
    
    if db is not None:
        return
        
    if config is None:
        # Default configuration if none provided
        config = {
            'name': 'cc.sqlite3',
            'pragmas': {
                'journal_mode': 'wal',
                'cache_size': -1024 * 64  # 64MB
            }
        }
    
    db = SqliteDatabase(
        config['name'],
        pragmas=config['pragmas'],
        autoconnect=False,
    )
    
    with db:
        router = Router(db, migrate_dir='storages/migrations')
        router.run()
