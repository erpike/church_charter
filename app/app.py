import os

from flask import Flask

from app.auth.auth import init_auth
from app.routes.routes import init_routes
from config import get_config
from config.logging_config import setup_logging
from storages.database import init_db


def create_app(test_config=None):
    app = Flask(
        __name__,
        template_folder=os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "templates"
        ),
        static_folder=os.path.join(os.path.dirname(__file__), "static"),
    )

    # Load configuration
    if test_config is None:
        app.config.from_object(get_config())
    else:
        app.config.update(test_config)

    # add session secret key
    app.config["SECRET_KEY"] = "your-secret-key-here"

    # Setup logging
    logger = setup_logging(app)

    try:
        logger.info("Initializing database...")
        init_db(app.config.get("DATABASE"))
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

    logger.info("Initializing auth...")
    init_auth(app)
    logger.info("Initializing routes...")
    init_routes(app)

    return app
