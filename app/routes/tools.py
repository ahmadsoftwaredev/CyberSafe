from flask import Blueprint, render_template
from flask_login import login_required

tools = Blueprint("tools", __name__)


@tools.route("/password-checker")
@login_required
def password_checker():
    return render_template("password_checker.html")


@tools.route("/url-checker")
@login_required
def url_checker():
    return render_template("url_checker.html")