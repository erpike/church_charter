import os
import glob
from datetime import datetime
from peewee import SqliteDatabase
from .models import db


class MigrationManager:
    def __init__(self, db: SqliteDatabase, migrations_dir: str = "storages/migrations"):
        self.db = db
        self.migrations_dir = migrations_dir
        self._ensure_migrations_table()
    
    def _ensure_migrations_table(self):
        """Create migrations table if it doesn't exist."""
        self.db.execute_sql("""
            CREATE TABLE IF NOT EXISTS migrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    
    def _get_applied_migrations(self):
        """Get list of already applied migrations."""
        cursor = self.db.execute_sql("SELECT name FROM migrations")
        return {row[0] for row in cursor.fetchall()}
    
    def _get_migration_files(self):
        """Get all SQL migration files sorted by name."""
        pattern = os.path.join(self.migrations_dir, '*.sql')
        return sorted(glob.glob(pattern))
    
    def _read_migration_file(self, file_path):
        """Read and return the contents of a migration file."""
        with open(file_path, 'r') as f:
            return f.read()
    
    def validate_migrations(self):
        """Validate that all migration files are properly tracked in the database."""
        applied = self._get_applied_migrations()
        migration_files = {os.path.basename(f) for f in self._get_migration_files()}
        
        # Check for orphaned migrations in database
        if orphaned_in_db := (applied - migration_files):
            print("Warning: The following migrations are tracked in the database but files are missing:")
            for migration in sorted(orphaned_in_db):
                print(f"  - {migration}")
            raise Exception("Migration validation failed. Please check the warnings above.")


    def run_migrations(self):
        """Run all pending migrations."""
        # First validate migrations
        self.validate_migrations()
            
        applied = self._get_applied_migrations()
        migration_files = self._get_migration_files()
        
        for migration_file in migration_files:
            migration_name = os.path.basename(migration_file)
            
            if migration_name not in applied:
                print(f"Applying migration: {migration_name}")
                
                # Read and execute the migration
                sql = self._read_migration_file(migration_file)
                
                try:
                    with self.db.atomic():
                        # Execute the migration SQL
                        self.db.execute_sql(sql)
                        
                        # Record the migration
                        self.db.execute_sql(
                            "INSERT INTO migrations (name) VALUES (?)",
                            (migration_name,)
                        )
                    
                    print(f"Successfully applied migration: {migration_name}")
                except Exception as e:
                    print(f"Error applying migration {migration_name}: {str(e)}")
                    raise
