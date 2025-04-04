CREATE TABLE IF NOT EXISTS canon (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT (datetime('now', 'utc')),
    updated_at TIMESTAMP DEFAULT (datetime('now', 'utc'))
);
