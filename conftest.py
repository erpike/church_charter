import os
import sys
import tempfile

import pytest

from app.app import create_app
from storages.database import init_db

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


@pytest.fixture
def temp_db_file():
    """Create a temporary database file for testing."""
    fd, path = tempfile.mkstemp(suffix=".sqlite")
    os.close(fd)
    try:
        yield path
    finally:
        # Clean up the temporary file after the test, even if the test fails
        if os.path.exists(path):
            os.unlink(path)


@pytest.fixture
def test_config(temp_db_file):
    """Test configuration that overrides the default config."""
    return {
        "TESTING": True,
        "DATABASE": {"name": temp_db_file, "pragmas": {}, "autoconnect": True},
        "DEBUG": False,
        "ADMIN_USERNAME": "admin",
        "ADMIN_PASSWORD": "pass",
        # Add any other test-specific configuration here
    }


@pytest.fixture
def app(test_config):
    """Create and configure a new app instance for each test."""
    return create_app(test_config)


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def init_test_db(test_config):
    init_db(test_config["DATABASE"])
