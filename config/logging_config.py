import logging
import logging.handlers
from pathlib import Path

# Create logs directory if it doesn't exist
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Log file path
log_file = log_dir / "app.log"

# Logging format
log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def setup_logging(app):
    """Configure logging for the application."""
    # Set the base logging level
    app.logger.setLevel(logging.INFO)

    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=10485760, backupCount=5  # 10MB
    )
    file_handler.setFormatter(log_format)
    file_handler.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    console_handler.setLevel(logging.INFO)

    # Add handlers to the app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)

    # Log application startup
    app.logger.info("Application startup")

    return app.logger
