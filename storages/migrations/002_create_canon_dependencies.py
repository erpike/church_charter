def migrate(migrator, database, **kwargs):
    """Write your migrations here."""

    database.execute_sql("""
        CREATE TABLE IF NOT EXISTS canonchapter (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            canon_id INTEGER NOT NULL, 
            title VARCHAR(255) NOT NULL,
            position INTEGER NOT NULL DEFAULT 0,
            type VARCHAR(32) NOT NULL CHECK (type IN ('song', 'troparion', 'kontakion', 'stichos')),
            created_at TIMESTAMP DEFAULT (datetime('now', 'utc')),
            updated_at TIMESTAMP DEFAULT (datetime('now', 'utc')),
            FOREIGN KEY (canon_id) REFERENCES canon(id) ON DELETE CASCADE
        )
    """)
    database.execute_sql("""
        CREATE TABLE IF NOT EXISTS canonitem (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chapter_id INTEGER NOT NULL, 
            type VARCHAR(32) NOT NULL CHECK (
                type IN ('refrain', 'hirmos', 'ikos', 'song', 'troparion', 'kontakion', 'stichos')
            ),
            text TEXT NOT NULL,
            position INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT (datetime('now', 'utc')),
            updated_at TIMESTAMP DEFAULT (datetime('now', 'utc')),
            FOREIGN KEY (chapter_id) REFERENCES canonchapter(id) ON DELETE CASCADE
        )
    """)

def rollback(migrator, database, **kwargs):
    """Write your rollback migrations here."""
    database.execute_sql("DROP TABLE IF EXISTS canonitem")
    database.execute_sql("DROP TABLE IF EXISTS canonchapter")
