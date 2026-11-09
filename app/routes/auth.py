
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models import User

auth = Blueprint("auth", __name__)


# --------------------------------
# ROLE-BASED DASHBOARD REDIRECTION
# --------------------------------

def dashboard_redirect(user):

    if user.role == "admin":
        return redirect(url_for("main.admin_dashboard"))

    return redirect(url_for("main.dashboard"))


@auth.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return dashboard_redirect(current_user)

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not username or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for("auth.register"))

        if len(username) > 80:
            flash("Username must be 80 characters or fewer.", "danger")
            return redirect(url_for("auth.register"))

        if len(email) > 120 or "@" not in email:
            flash("Please enter a valid email address.", "danger")
            return redirect(url_for("auth.register"))

        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "danger")
            return redirect(url_for("auth.register"))

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("auth.register"))

        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            flash("Username or email already exists.", "danger")
            return redirect(url_for("auth.register"))

        password_hash = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            role="user"
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return dashboard_redirect(current_user)

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):

            login_user(user)

            flash("Welcome back!", "success")

            return dashboard_redirect(user)

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


@auth.route("/logout", methods=["POST"])
@login_required
def logout():

    logout_user()

    flash("You have been logged out.", "success")

    return redirect(url_for("main.home"))
