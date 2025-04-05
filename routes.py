from flask import abort, render_template

from storages.database import db
from storages.models import Canon, CanonChapter, CanonItem


def init_routes(app):
    """Initialize routes for the application."""

    @app.route("/")
    def index():
        app.logger.info("Index endpoint called")
        with db:
            canons = list(Canon.select().order_by(Canon.created_at.desc()))
        return render_template("index.html", canons=canons)

    @app.route("/canon/<int:canon_id>")
    def canon_detail(canon_id):
        app.logger.info(f"Canon detail endpoint called for canon_id: {canon_id}")
        with db:
            canon = Canon.get_or_none(Canon.id == canon_id)
            if canon is None:
                abort(404)
            return render_template(
                "canon_detail.html",
                canon=canon,
                CanonChapter=CanonChapter,
                CanonItem=CanonItem,
            )
