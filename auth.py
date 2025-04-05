from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from storages.database import db
from storages.models import User

# create Blueprint
auth_bp = Blueprint("auth", __name__)


def load_user(user_id):
    with db:
        return User.get_or_none(User.id == user_id)


def init_auth(app):
    """Initialize authentication for the application."""
    # set up Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Будь ласка, увійдіть для доступу до цієї сторінки."
    login_manager.user_loader(load_user)

    # Blueprint register
    app.register_blueprint(auth_bp)

    # create admin if he does not exist
    with db:
        if not User.select().where(User.username == "admin").exists():
            admin = User(username="admin")
            admin.set_password("admin_password")
            admin.save()
            app.logger.info("Admin user created")

    return login_manager


# auth routes
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        with db:
            user = User.get_or_none(User.username == username)

        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("index"))
        else:
            flash("Невірне ім'я користувача або пароль")

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
