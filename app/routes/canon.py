from io import BytesIO

from docx import Document
from flask import (
    Blueprint,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from flask_login import login_required

from storages.database import db
from storages.models import (
    AggregatedCanon,
    Canon,
    CanonChapter,
    CanonChapterGroup,
    CanonChapterType,
    CanonItem,
    CanonItemType,
)

# Create Blueprint
canon_bp = Blueprint("canon", __name__, url_prefix="/canon")


@canon_bp.route("/<int:canon_id>")
def detail(canon_id):
    """Display details of a specific canon."""
    with db:
        canon = Canon.get_or_none(Canon.id == canon_id)
        if canon is None:
            abort(404)

        # Get sorted content using the get_data method
        content = canon.get_data()

        return render_template(
            "canon_detail.html",
            canon=canon,
            content=content,
        )


@canon_bp.route("/<int:canon_id>/chapter/create", methods=["GET", "POST"])
@login_required
def create_chapter(canon_id):
    """Create a new chapter in a canon."""
    with db:
        canon = Canon.get_or_none(Canon.id == canon_id)
        if canon is None:
            flash("Канон не знайдено", "error")
            return redirect(url_for("canon.detail", canon_id=canon_id))

        if request.method == "POST":
            title = request.form.get("title")
            chapter_type = request.form.get("type")
            group = request.form.get("group")
            position = request.form.get("position", 0)

            if not title or not chapter_type or not group:
                flash("Всі поля повинні бути заповнені", "error")
                return redirect(url_for("canon.create_chapter", canon_id=canon_id))

            try:
                position = int(position)
            except ValueError:
                position = 0

            CanonChapter.create(
                canon=canon,
                title=title,
                type=chapter_type,
                group=group,
                position=position,
            )
            flash("Главу успішно створено", "success")
            return redirect(url_for("canon.detail", canon_id=canon_id))

        return render_template(
            "canon/chapter_form.html",
            canon=canon,
            chapter_types=CanonChapterType,
            chapter_groups=CanonChapterGroup,
        )


@canon_bp.route("/chapter/<int:chapter_id>/edit", methods=["GET", "POST"])
@login_required
def edit_chapter(chapter_id):
    """Edit an existing chapter."""
    with db:
        chapter = CanonChapter.get_or_none(CanonChapter.id == chapter_id)
        if chapter is None:
            flash("Главу не знайдено", "error")
            return redirect(url_for("canon.detail", canon_id=chapter.canon.id))

        if request.method == "POST":
            title = request.form.get("title")
            chapter_type = request.form.get("type")
            group = request.form.get("group")
            position = request.form.get("position", 0)

            if not title or not chapter_type or not group:
                flash("Всі поля повинні бути заповнені", "error")
                return redirect(url_for("canon.edit_chapter", chapter_id=chapter_id))

            try:
                position = int(position)
            except ValueError:
                position = 0

            chapter.title = title
            chapter.type = chapter_type
            chapter.group = group
            chapter.position = position
            chapter.save()

            flash("Главу успішно оновлено", "success")
            return redirect(url_for("canon.detail", canon_id=chapter.canon.id))

        return render_template(
            "canon/chapter_form.html",
            canon=chapter.canon,
            chapter=chapter,
            chapter_types=CanonChapterType,
            chapter_groups=CanonChapterGroup,
        )


@canon_bp.route("/chapter/<int:chapter_id>/delete", methods=["POST"])
@login_required
def delete_chapter(chapter_id):
    """Delete a chapter."""
    with db:
        chapter = CanonChapter.get_or_none(CanonChapter.id == chapter_id)
        if chapter is None:
            flash("Главу не знайдено", "error")
            return redirect(url_for("canon.detail", canon_id=chapter.canon.id))

        canon_id = chapter.canon.id
        chapter.delete_instance()
        flash("Главу успішно видалено", "success")
        return redirect(url_for("canon.detail", canon_id=canon_id))


@canon_bp.route("/chapter/<int:chapter_id>/item/create", methods=["GET", "POST"])
@login_required
def create_item(chapter_id):
    """Create a new item in a chapter."""
    with db:
        chapter = CanonChapter.get_or_none(CanonChapter.id == chapter_id)
        if chapter is None:
            flash("Главу не знайдено", "error")
            return redirect(url_for("canon.detail", canon_id=chapter.canon.id))

        if request.method == "POST":
            item_type = request.form.get("type")
            text = request.form.get("text")
            position = request.form.get("position", 0)

            if not text or not item_type:
                flash("Всі поля повинні бути заповнені", "error")
                return redirect(url_for("canon.create_item", chapter_id=chapter_id))

            try:
                position = int(position)
            except ValueError:
                position = 0

            CanonItem.create(
                chapter=chapter, type=item_type, text=text, position=position
            )
            flash("Елемент успішно створено", "success")
            return redirect(url_for("canon.detail", canon_id=chapter.canon.id))

        return render_template(
            "canon/item_form.html",
            chapter=chapter,
            item_types=CanonItemType,
        )


@canon_bp.route("/item/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_item(item_id):
    """Edit an existing item."""
    with db:
        item = CanonItem.get_or_none(CanonItem.id == item_id)
        if item is None:
            flash("Елемент не знайдено", "error")
            return redirect(url_for("canon.detail", canon_id=item.chapter.canon.id))

        if request.method == "POST":
            item_type = request.form.get("type")
            text = request.form.get("text")
            position = request.form.get("position", 0)

            if not text or not item_type:
                flash("Всі поля повинні бути заповнені", "error")
                return redirect(url_for("canon.edit_item", item_id=item_id))

            try:
                position = int(position)
            except ValueError:
                position = 0

            item.type = item_type
            item.text = text
            item.position = position
            item.save()

            flash("Елемент успішно оновлено", "success")
            return redirect(url_for("canon.detail", canon_id=item.chapter.canon.id))

        return render_template(
            "canon/item_form.html",
            chapter=item.chapter,
            item=item,
            item_types=CanonItemType,
        )


@canon_bp.route("/item/<int:item_id>/delete", methods=["POST"])
@login_required
def delete_item(item_id):
    """Delete an item."""
    with db:
        item = CanonItem.get_or_none(CanonItem.id == item_id)
        if item is None:
            flash("Елемент не знайдено", "error")
            return redirect(url_for("canon.detail", canon_id=item.chapter.canon.id))

        canon_id = item.chapter.canon.id
        item.delete_instance()
        flash("Елемент успішно видалено", "success")
        return redirect(url_for("canon.detail", canon_id=canon_id))


@canon_bp.route("/chapter/<int:chapter_id>/update-items-order", methods=["POST"])
@login_required
def update_items_order(chapter_id):
    """Update the order of items in a chapter."""
    with db:
        chapter = CanonChapter.get_or_none(CanonChapter.id == chapter_id)
        if chapter is None:
            return jsonify({"success": False, "message": "Главу не знайдено"}), 404

        data = request.get_json()
        if not data or "items" not in data:
            return (
                jsonify({"success": False, "message": "Неправильний формат даних"}),
                400,
            )

        try:
            for item_data in data["items"]:
                item_id = item_data.get("id")
                position = item_data.get("position", 0)

                item = CanonItem.get_or_none(CanonItem.id == item_id)
                if item and item.chapter.id == chapter_id:
                    item.position = position
                    item.save()

            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500


@canon_bp.route("/<int:canon_id>/download-docx")
def download_docx(canon_id):
    """Download canon as a .docx file."""
    with db:
        canon = Canon.get_or_none(Canon.id == canon_id)
        if canon is None:
            abort(404)

        # Create a new Document
        doc = Document()

        # Add title
        doc.add_heading(canon.name, 0)

        # Add chapters and their items
        for chapter in canon.chapters.order_by(CanonChapter.position):
            # Add chapter title
            doc.add_heading(chapter.title, level=1)

            # Add items
            for item in chapter.items.order_by(CanonItem.position):
                if item.type == "hirmos":
                    doc.add_paragraph(f"Ирмос: {item.text}")
                elif item.type == "refrain":
                    doc.add_paragraph(f"Припев: {item.text}")
                else:
                    doc.add_paragraph(item.text)

            # Add a separator between chapters
            doc.add_paragraph()

        # Save the document to a BytesIO object
        doc_io = BytesIO()
        doc.save(doc_io)
        doc_io.seek(0)

        # Return the document as a downloadable file
        return send_file(
            doc_io,
            mimetype=(
                "application/vnd.openxmlformats-officedocument"
                ".wordprocessingml.document"
            ),
            as_attachment=True,
            download_name=f"{canon.name}.docx",
        )


@canon_bp.route("/aggregated/create", methods=["GET", "POST"])
@login_required
def create_aggregated_canon():
    """Create a new aggregated canon."""
    with db:
        if request.method == "POST":
            name = request.form.get("name")
            if not name:
                flash("Назва зведеного канону не може бути порожньою", "error")
                return redirect(url_for("canon.create_aggregated_canon"))

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
                    url_for("canon.detail_aggregated", canon_id=existing_canon.id)
                )

            # Create the aggregated canon
            aggregated_canon = AggregatedCanon.create(
                name=name, canon_ids=canon_ids_str
            )

            flash("Зведений канон успішно створено", "success")
            return redirect(
                url_for("canon.detail_aggregated", canon_id=aggregated_canon.id)
            )

        # Get all canons for the dropdown
        canons = list(Canon.select().order_by(Canon.name))
        return render_template(
            "canon/aggregated_form.html",
            canons=canons,
        )


@canon_bp.route("/aggregated/<int:canon_id>")
def detail_aggregated(canon_id):
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


@canon_bp.route("/aggregated/<int:canon_id>/edit", methods=["GET", "POST"])
@login_required
def edit_aggregated_canon(canon_id):
    """Edit an existing aggregated canon."""
    with db:
        canon = AggregatedCanon.get_or_none(AggregatedCanon.id == canon_id)
        if canon is None:
            flash("Зведений канон не знайдено", "error")
            return redirect(url_for("canon.detail_aggregated", canon_id=canon_id))

        if request.method == "POST":
            name = request.form.get("name")
            if not name:
                flash("Назва зведеного канону не може бути порожньою", "error")
                return redirect(
                    url_for("canon.edit_aggregated_canon", canon_id=canon_id)
                )

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
                    url_for("canon.detail_aggregated", canon_id=existing_canon.id)
                )

            # Update the aggregated canon
            canon.name = name
            canon.canon_ids = canon_ids_str
            canon.save()

            flash("Зведений канон успішно оновлено", "success")
            return redirect(url_for("canon.detail_aggregated", canon_id=canon.id))

        # Get all canons for the dropdown
        all_canons = list(Canon.select().order_by(Canon.name))

        # Get current canon IDs and their positions
        current_canon_ids = canon.canon_ids.split(",")
        current_links = [
            {"canon_id": canon_id, "position": pos}
            for pos, canon_id in enumerate(current_canon_ids)
        ]

        return render_template(
            "canon/aggregated_form.html",
            canon=canon,
            canons=all_canons,
            current_links=current_links,
        )


@canon_bp.route("/aggregated/<int:canon_id>/delete", methods=["POST"])
@login_required
def delete_aggregated_canon(canon_id):
    """Delete an aggregated canon."""
    with db:
        canon = AggregatedCanon.get_or_none(AggregatedCanon.id == canon_id)
        if canon is None:
            flash("Зведений канон не знайдено", "error")
            return redirect(url_for("canon.detail_aggregated", canon_id=canon_id))

        canon.delete_instance()
        flash("Зведений канон успішно видалено", "success")
        return redirect(url_for("canon.detail_aggregated", canon_id=canon_id))
