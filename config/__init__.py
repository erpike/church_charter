"""Configuration factory."""

import os

from config.development import DevelopmentConfig
from config.production import ProductionConfig

# Configuration dictionary
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config():
    """Get configuration based on environment."""
    env = os.environ.get("FLASK_ENV", "default")
    return config[env]
