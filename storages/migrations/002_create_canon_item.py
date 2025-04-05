def migrate(migrator, database, **kwargs):
    """Write your migrations here."""
    database.execute_sql("""
        CREATE TABLE IF NOT EXISTS canonitem (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            canon_id INTEGER NOT NULL, 
            type VARCHAR(255) NOT NULL CHECK (
                type IN ('hirmos', 'ikos', 'song', 'troparion', 'kontakion', 'stichos')
            ),
            text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT (datetime('now', 'utc')),
            updated_at TIMESTAMP DEFAULT (datetime('now', 'utc')),
            FOREIGN KEY (canon_id) REFERENCES canon(id) ON DELETE CASCADE
        )
    """)

def rollback(migrator, database, **kwargs):
    """Write your rollback migrations here."""
    database.execute_sql("DROP TABLE IF EXISTS canonitem")
