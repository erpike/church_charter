import pytest

from app import create_app
from config import get_config


@pytest.fixture
def test_config():
    """Test configuration that overrides the default config."""
    return {
        "TESTING": True,
        "DATABASE": {"name": ":memory:", "pragmas": {}},
        "DEBUG": False,
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


def test_hello_world(client):
    """Test the hello world endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == b"Hello, World!"


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
