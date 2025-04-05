from flask import Flask

from config import get_config
from config.logging_config import setup_logging
from routes import init_routes
from storages.database import init_db


def create_app(test_config=None):
    app = Flask(__name__)

    # Load configuration
    if test_config is None:
        app.config.from_object(get_config())
    else:
        app.config.update(test_config)

    # Setup logging
    logger = setup_logging(app)

    # Initialize database
    try:
        logger.info("Initializing database...")
        init_db(app.config.get("DATABASE"))
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

    # Initialize routes
    init_routes(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=app.config["DEBUG"])
