from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from storages.database import db
from storages.models import Canon

# Create Blueprint
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
@login_required
def dashboard():
    """Admin dashboard view."""
    with db:
        canons = list(Canon.select().order_by(Canon.created_at.desc()))
    return render_template("admin/dashboard.html", canons=canons)


@admin_bp.route("/canon/create", methods=["GET", "POST"])
@login_required
def create_canon():
    """Create a new canon."""
    if request.method == "POST":
        name = request.form.get("name")
        if not name:
            flash("Назва канону не може бути порожньою", "error")
            return redirect(url_for("admin.create_canon"))

        with db:
            Canon.create(name=name)
            flash("Канон успішно створено", "success")
            return redirect(url_for("admin.dashboard"))

    return render_template("admin/canon_form.html")


@admin_bp.route("/canon/<int:canon_id>/edit", methods=["GET", "POST"])
@login_required
def edit_canon(canon_id):
    """Edit an existing canon."""
    with db:
        canon = Canon.get_or_none(Canon.id == canon_id)
        if canon is None:
            flash("Канон не знайдено", "error")
            return redirect(url_for("admin.dashboard"))

        if request.method == "POST":
            name = request.form.get("name")
            if not name:
                flash("Назва канону не може бути порожньою", "error")
                return redirect(url_for("admin.edit_canon", canon_id=canon_id))

            canon.name = name
            canon.save()
            flash("Канон успішно оновлено", "success")
            return redirect(url_for("admin.dashboard"))

        return render_template("admin/canon_form.html", canon=canon)


@admin_bp.route("/canon/<int:canon_id>/delete", methods=["POST"])
@login_required
def delete_canon(canon_id):
    """Delete a canon."""
    with db:
        canon = Canon.get_or_none(Canon.id == canon_id)
        if canon is None:
            flash("Канон не знайдено", "error")
            return redirect(url_for("admin.dashboard"))

        canon.delete_instance()
        flash("Канон успішно видалено", "success")
        return redirect(url_for("admin.dashboard"))
