from functools import wraps

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, abort
)
from flask_login import login_required, current_user

from app.extensions import db
from app.models import SecurityTip

tips = Blueprint("tips", __name__)


# Admin-only access decorator
def admin_required(view_function):
    @wraps(view_function)
    @login_required
    def decorated_function(*args, **kwargs):

        if current_user.role != "admin":
            abort(403)

        return view_function(*args, **kwargs)

    return decorated_function


# User: View all tips
@tips.route("/tips")
@login_required
def list_tips():

    all_tips = SecurityTip.query.order_by(
        SecurityTip.created_at.desc()
    ).all()

    return render_template("tips.html", tips=all_tips)


# User: Read one article
@tips.route("/tips/<int:tip_id>")
@login_required
def tip_detail(tip_id):

    tip = db.get_or_404(SecurityTip, tip_id)

    return render_template("tip_detail.html", tip=tip)


# Admin: Manage tips
@tips.route("/admin/tips")
@admin_required
def admin_tips():

    all_tips = SecurityTip.query.order_by(
        SecurityTip.created_at.desc()
    ).all()

    return render_template("admin/tips.html", tips=all_tips)


# Admin: Add tip
@tips.route("/admin/tips/add", methods=["GET", "POST"])
@admin_required
def add_tip():

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not category or not content:
            flash("All fields are required.", "danger")
            return redirect(url_for("tips.add_tip"))

        if len(title) > 200 or len(category) > 100:
            flash("Title or category is too long.", "danger")
            return redirect(url_for("tips.add_tip"))

        new_tip = SecurityTip(
            title=title,
            category=category,
            content=content
        )

        db.session.add(new_tip)
        db.session.commit()

        flash("Security tip added successfully!", "success")
        return redirect(url_for("tips.admin_tips"))

    return render_template("admin/add_tip.html")


# Admin: Edit tip
@tips.route("/admin/tips/edit/<int:tip_id>", methods=["GET", "POST"])
@admin_required
def edit_tip(tip_id):

    tip = db.get_or_404(SecurityTip, tip_id)

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not category or not content:
            flash("All fields are required.", "danger")
            return redirect(
                url_for("tips.edit_tip", tip_id=tip.id)
            )

        if len(title) > 200 or len(category) > 100:
            flash("Title or category is too long.", "danger")
            return redirect(
                url_for("tips.edit_tip", tip_id=tip.id)
            )

        tip.title = title
        tip.category = category
        tip.content = content

        db.session.commit()

        flash("Security tip updated successfully!", "success")
        return redirect(url_for("tips.admin_tips"))

    return render_template("admin/edit_tip.html", tip=tip)


# Admin: Delete tip
@tips.route("/admin/tips/delete/<int:tip_id>", methods=["POST"])
@admin_required
def delete_tip(tip_id):

    tip = db.get_or_404(SecurityTip, tip_id)

    db.session.delete(tip)
    db.session.commit()

    flash("Security tip deleted successfully!", "success")

    return redirect(url_for("tips.admin_tips"))