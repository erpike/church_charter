from unittest import mock
from unittest.mock import call

from app.app import create_app
from config import get_config


def test_index(client):
    """Test the hello world endpoint."""
    with mock.patch("app.routes.routes.render_template") as m:
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
