from flask import Blueprint, abort, render_template

from storages.database import db
from storages.models import Canon, CanonChapter, CanonItem

# Create Blueprint
canon_bp = Blueprint("canon", __name__, url_prefix="/canon")


@canon_bp.route("/<int:canon_id>")
def detail(canon_id):
    """Display details of a specific canon."""
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
