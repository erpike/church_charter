from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required

from storages.database import db
from storages.models import AggregatedCanon, Canon

# Create Blueprint
aggregated_canon_bp = Blueprint(
    "aggregated_canon", __name__, url_prefix="/canon/aggregated"
)


@aggregated_canon_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """Create a new aggregated canon."""
    with db:
        if request.method == "POST":
            name = request.form.get("name")
            if not name:
                flash("Назва зведеного канону не може бути порожньою", "error")
                return redirect(url_for("aggregated_canon.create"))

            # Get selected canons and their positions
            canon_ids = request.form.getlist("canon_ids[]")
            positions = request.form.getlist("positions[]")

            # Convert to list of tuples (canon_id, position) and sort by position
            canon_positions = list(zip(canon_ids, positions))
            canon_positions.sort(key=lambda x: int(x[1]))

            # Extract sorted canon IDs
            sorted_canon_ids = [canon_id for canon_id, _ in canon_positions]
            canon_ids_str = ",".join(sorted_canon_ids)

            # Check if this combination already exists
            existing_canon = AggregatedCanon.find_existing_combination(sorted_canon_ids)
            if existing_canon:
                flash("Такий зведений канон вже існує", "info")
                return redirect(
                    url_for("aggregated_canon.detail", canon_id=existing_canon.id)
                )

            # Create the aggregated canon
            aggregated_canon = AggregatedCanon.create(
                name=name, canon_ids=canon_ids_str
            )

            flash("Зведений канон успішно створено", "success")
            return redirect(
                url_for("aggregated_canon.detail", canon_id=aggregated_canon.id)
            )

        # Get all canons for the dropdown
        canons = list(Canon.select().order_by(Canon.name))
        return render_template(
            "canon/aggregated_form.html",
            canons=canons,
            current_links=[],
        )


@aggregated_canon_bp.route("/<int:canon_id>")
def detail(canon_id):
    """Display details of a specific aggregated canon."""
    with db:
        canon = AggregatedCanon.get_or_none(AggregatedCanon.id == canon_id)
        if canon is None:
            abort(404)

        # Get sorted content using the get_data method
        content = canon.get_data()

        return render_template(
            "canon/aggregated_detail.html",
            canon=canon,
            content=content,
        )


@aggregated_canon_bp.route("/<int:canon_id>/edit", methods=["GET", "POST"])
@login_required
def edit(canon_id):
    """Edit an existing aggregated canon."""
    with db:
        canon = AggregatedCanon.get_or_none(AggregatedCanon.id == canon_id)
        if canon is None:
            flash("Зведений канон не знайдено", "error")
            return redirect(url_for("aggregated_canon.detail", canon_id=canon_id))

        if request.method == "POST":
            name = request.form.get("name")
            if not name:
                flash("Назва зведеного канону не може бути порожньою", "error")
                return redirect(url_for("aggregated_canon.edit", canon_id=canon_id))

            # Get selected canons and their positions
            canon_ids = request.form.getlist("canon_ids[]")
            positions = request.form.getlist("positions[]")

            # Convert to list of tuples (canon_id, position) and sort by position
            canon_positions = list(zip(canon_ids, positions))
            canon_positions.sort(key=lambda x: int(x[1]))

            # Extract sorted canon IDs
            sorted_canon_ids = [canon_id for canon_id, _ in canon_positions]
            canon_ids_str = ",".join(sorted_canon_ids)

            # Check if this combination already exists (excluding current canon)
            existing_canon = AggregatedCanon.find_existing_combination(sorted_canon_ids)
            if existing_canon and existing_canon.id != canon.id:
                flash("Такий зведений канон вже існує", "info")
                return redirect(
                    url_for("aggregated_canon.detail", canon_id=existing_canon.id)
                )

            # Update the aggregated canon
            canon.name = name
            canon.canon_ids = canon_ids_str
            canon.save()

            flash("Зведений канон успішно оновлено", "success")
            return redirect(url_for("aggregated_canon.detail", canon_id=canon.id))

        # Get all canons for the dropdown
        all_canons = list(Canon.select().order_by(Canon.name))

        # Get current canon IDs and their positions
        current_canon_ids = canon.canon_ids.split(",") if canon.canon_ids else []
        current_links = [
            {
                "canon_id": canon_id,
                "canon_name": Canon.get_by_id(canon_id).name,
                "position": pos,
            }
            for pos, canon_id in enumerate(current_canon_ids)
        ]

        return render_template(
            "canon/aggregated_form.html",
            canon=canon,
            canons=all_canons,
            current_links=current_links,
        )


@aggregated_canon_bp.route("/<int:canon_id>/delete", methods=["POST"])
@login_required
def delete(canon_id):
    """Delete an aggregated canon."""
    with db:
        canon = AggregatedCanon.get_or_none(AggregatedCanon.id == canon_id)
        if canon is None:
            flash("Зведений канон не знайдено", "error")
            return redirect(url_for("aggregated_canon.detail", canon_id=canon_id))

        canon.delete_instance()
        flash("Зведений канон успішно видалено", "success")
        return redirect(url_for("admin.dashboard", canon_id=canon_id))
