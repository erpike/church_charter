from flask import Flask
from storages.database import init_db

app = Flask(__name__)

# Initialize database and run migrations
init_db()


@app.route('/')
def hello_world():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)
