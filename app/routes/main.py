from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user

from app.models import User, SecurityTip, Quiz, Question, QuizResult

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/about")
def about():
    return "<h1>About CyberSafe</h1><p>Learn how to stay safe online.</p>"


@main.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


# --------------------------------
# ADMIN: SYSTEM OVERVIEW
# --------------------------------

@main.route("/admin/dashboard")
@login_required
def admin_dashboard():

    # Only administrators can access this dashboard
    if current_user.role != "admin":
        abort(403)

    # System Statistics
    total_users = User.query.count()

    total_articles = SecurityTip.query.count()

    total_quizzes = Quiz.query.count()

    total_questions = Question.query.count()

    total_attempts = QuizResult.query.count()

    stats = {
        "total_users": total_users,
        "total_articles": total_articles,
        "total_quizzes": total_quizzes,
        "total_questions": total_questions,
        "total_attempts": total_attempts
    }

    return render_template(
        "admin_dashboard.html",
        stats=stats
    )