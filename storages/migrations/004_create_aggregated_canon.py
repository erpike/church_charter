def migrate(migrator, database, **kwargs):
    """Write your migrations here."""
    database.execute_sql("""
        CREATE TABLE IF NOT EXISTS aggregatedcanon (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            canon_ids TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT (datetime('now', 'utc')),
            updated_at TIMESTAMP DEFAULT (datetime('now', 'utc'))
        )
    """)

def rollback(migrator, database, **kwargs):
    """Write your rollback migrations here."""
    database.execute_sql("DROP TABLE IF EXISTS aggregatedcanon")
