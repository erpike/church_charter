from flask import Flask
from storages.models import db
from storages.migration_manager import MigrationManager

app = Flask(__name__)

# Initialize database and run migrations
db.connect()
migration_manager = MigrationManager(db)
migration_manager.run_migrations()
db.close()


@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
