def migrate(migrator, database, **kwargs):
    """Create users table."""
    database.execute_sql("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(80) NOT NULL UNIQUE,
            password_hash VARCHAR(128) NOT NULL,
            created_at TIMESTAMP DEFAULT (datetime('now', 'utc')),
            updated_at TIMESTAMP DEFAULT (datetime('now', 'utc'))
        )
    """)

def rollback(migrator, database, **kwargs):
    """Drop users table."""
    database.execute_sql("DROP TABLE IF EXISTS user")
