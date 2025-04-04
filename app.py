from flask import Flask
from storages.database import init_db, db


def create_app(test_config=None):
    app = Flask(__name__)
    
    # Load configuration
    if test_config is None:
        app.config.from_object('config.default')
    else:
        app.config.update(test_config)
    
    # Initialize database
    try:
        init_db(app.config.get('DATABASE'))
    except Exception as e:
        app.logger.error(f"Failed to initialize database: {e}")
        raise
    
    @app.route('/')
    def hello_world():
        return "Hello, World!"
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
