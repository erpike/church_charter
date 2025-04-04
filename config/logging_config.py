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


def get_log_level(level_name):
    """Convert string log level to logging level constant."""
    return getattr(logging, level_name.upper(), logging.INFO)


def setup_logging(app):
    """Configure logging for the application."""
    # Get log levels from config
    base_level = get_log_level(app.config.get("LOG_LEVEL", "INFO"))
    file_level = get_log_level(app.config.get("LOG_FILE_LEVEL", "INFO"))
    console_level = get_log_level(app.config.get("LOG_CONSOLE_LEVEL", "INFO"))

    # Set the base logging level
    app.logger.setLevel(base_level)

    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=10485760, backupCount=5  # 10MB
    )
    file_handler.setFormatter(log_format)
    file_handler.setLevel(file_level)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    console_handler.setLevel(console_level)

    # Add handlers to the app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)

    # Log application startup with configured levels
    app.logger.info(
        f"Application startup - Log levels: base={base_level}, "
        f"file={file_level}, console={console_level}"
    )

    return app.logger
