from flask import render_template

from storages.database import db
from storages.models import Canon

from .admin import admin_bp
from .canon import canon_bp


def init_routes(app):
    """Initialize routes for the application."""
    # Register blueprints
    app.register_blueprint(admin_bp)
    app.register_blueprint(canon_bp)

    @app.route("/")
    def index():
        """Display the home page with a list of all canons."""
        with db:
            canons = list(Canon.select().order_by(Canon.created_at.desc()))
        return render_template("index.html", canons=canons)
