import os
import tempfile
from unittest import mock
from unittest.mock import call

import pytest

from app import create_app
from config import get_config


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
        "DATABASE": {"name": temp_db_file, "pragmas": {}},
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


def test_index(client):
    """Test the hello world endpoint."""
    with mock.patch("routes.render_template") as m:
        response = client.get("/")
        assert response.status_code == 200
        assert m.call_count == 1
        assert m.call_args_list[0] == call("index.html", canons=[])


def test_app_creation(test_config):
    """Test that the app can be created with test config."""
    app = create_app(test_config)
    assert app.config["TESTING"] is True
    assert app.config["DEBUG"] is False


def test_app_uses_default_config():
    """Test that the app uses default config when no test_config is provided."""
    app = create_app()
    default_config = get_config()
    assert app.config["DEBUG"] == default_config.DEBUG
    assert app.config["DATABASE"] == default_config.DATABASE
