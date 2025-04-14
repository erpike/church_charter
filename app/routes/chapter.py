from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required

from storages.database import db
from storages.models import (
    Canon,
    CanonChapter,
    CanonChapterGroup,
    CanonChapterType,
    CanonItem,
    CanonItemType,
)

# Create Blueprint
chapter_bp = Blueprint("chapter", __name__, url_prefix="/chapter")


@chapter_bp.route("/<int:canon_id>/create", methods=["GET", "POST"])
@login_required
def create(canon_id):
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
                return redirect(url_for("chapter.create", canon_id=canon_id))

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


@chapter_bp.route("/<int:chapter_id>/edit", methods=["GET", "POST"])
@login_required
def edit(chapter_id):
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
                return redirect(url_for("chapter.edit", chapter_id=chapter_id))

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


@chapter_bp.route("/<int:chapter_id>/delete", methods=["POST"])
@login_required
def delete(chapter_id):
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


@chapter_bp.route("/<int:chapter_id>/item/create", methods=["GET", "POST"])
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
                return redirect(url_for("chapter.create_item", chapter_id=chapter_id))

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


@chapter_bp.route("/item/<int:item_id>/edit", methods=["GET", "POST"])
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
                return redirect(url_for("chapter.edit_item", item_id=item_id))

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


@chapter_bp.route("/item/<int:item_id>/delete", methods=["POST"])
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


@chapter_bp.route("/<int:chapter_id>/update-items-order", methods=["POST"])
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
