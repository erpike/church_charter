from flask import Flask
from storages.models import db
from peewee_migrate import Router

app = Flask(__name__)

# Initialize database and run migrations
db.connect()
router = Router(db, migrate_dir='storages/migrations')
router.run()
db.close()

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
