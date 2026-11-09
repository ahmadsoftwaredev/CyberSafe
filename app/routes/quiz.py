
from functools import wraps

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort
)

from flask_login import login_required, current_user

from app.extensions import db
from app.models import Quiz, Question, QuizResult, QuizAnswer


quiz = Blueprint("quiz", __name__)


# Admin-only access decorator
def admin_required(view_function):
    @wraps(view_function)
    @login_required
    def decorated_function(*args, **kwargs):

        if current_user.role != "admin":
            abort(403)

        return view_function(*args, **kwargs)

    return decorated_function


# --------------------------------
# ADMIN: VIEW ALL QUIZZES
# --------------------------------

@quiz.route("/admin/quizzes")
@admin_required
def admin_quizzes():

    all_quizzes = Quiz.query.order_by(
        Quiz.created_at.desc()
    ).all()

    return render_template(
        "admin/quizzes.html",
        quizzes=all_quizzes
    )


# --------------------------------
# ADMIN: ADD NEW QUIZ
# --------------------------------

@quiz.route("/admin/quizzes/add", methods=["GET", "POST"])
@admin_required
def add_quiz():

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()

        if not title or not category:
            flash("Quiz title and category are required.", "danger")
            return redirect(url_for("quiz.add_quiz"))

        if len(title) > 200 or len(category) > 100:
            flash("Title or category is too long.", "danger")
            return redirect(url_for("quiz.add_quiz"))

        new_quiz = Quiz(
            title=title,
            category=category,
            description=description,
            is_active=True
        )

        db.session.add(new_quiz)
        db.session.commit()

        flash("Quiz created successfully!", "success")

        return redirect(url_for("quiz.admin_quizzes"))

    return render_template("admin/add_quiz.html")


# --------------------------------
# ADMIN: EDIT QUIZ
# --------------------------------

@quiz.route(
    "/admin/quizzes/edit/<int:quiz_id>",
    methods=["GET", "POST"]
)
@admin_required
def edit_quiz(quiz_id):

    existing_quiz = db.get_or_404(Quiz, quiz_id)

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()

        if not title or not category:
            flash("Quiz title and category are required.", "danger")
            return redirect(
                url_for("quiz.edit_quiz", quiz_id=quiz_id)
            )

        if len(title) > 200 or len(category) > 100:
            flash("Title or category is too long.", "danger")
            return redirect(
                url_for("quiz.edit_quiz", quiz_id=quiz_id)
            )

        existing_quiz.title = title
        existing_quiz.category = category
        existing_quiz.description = description

        db.session.commit()

        flash("Quiz updated successfully!", "success")

        return redirect(url_for("quiz.admin_quizzes"))

    return render_template(
        "admin/edit_quiz.html",
        quiz=existing_quiz
    )


# --------------------------------
# ADMIN: DELETE QUIZ
# --------------------------------

@quiz.route(
    "/admin/quizzes/delete/<int:quiz_id>",
    methods=["POST"]
)
@admin_required
def delete_quiz(quiz_id):

    existing_quiz = db.get_or_404(Quiz, quiz_id)

    # Preserve quizzes linked to previous user results.
    if QuizResult.query.filter_by(quiz_id=quiz_id).first():
        flash(
            "This quiz has previous results. Deactivate it instead of deleting it.",
            "warning"
        )
        return redirect(url_for("quiz.admin_quizzes"))

    db.session.delete(existing_quiz)
    db.session.commit()

    flash("Quiz deleted successfully!", "success")

    return redirect(url_for("quiz.admin_quizzes"))


# --------------------------------
# ADMIN: VIEW QUIZ QUESTIONS
# --------------------------------

@quiz.route("/admin/quizzes/<int:quiz_id>/questions")
@admin_required
def manage_questions(quiz_id):

    existing_quiz = db.get_or_404(Quiz, quiz_id)

    questions = Question.query.filter_by(
        quiz_id=quiz_id
    ).order_by(Question.id.asc()).all()

    return render_template(
        "admin/questions.html",
        quiz=existing_quiz,
        questions=questions
    )


# --------------------------------
# ADMIN: ADD QUESTION
# --------------------------------

@quiz.route(
    "/admin/quizzes/<int:quiz_id>/questions/add",
    methods=["GET", "POST"]
)
@admin_required
def add_question(quiz_id):

    existing_quiz = db.get_or_404(Quiz, quiz_id)

    if request.method == "POST":

        question_text = request.form.get(
            "question_text", ""
        ).strip()

        option_a = request.form.get("option_a", "").strip()
        option_b = request.form.get("option_b", "").strip()
        option_c = request.form.get("option_c", "").strip()
        option_d = request.form.get("option_d", "").strip()

        correct_answer = request.form.get(
            "correct_answer", ""
        ).strip().upper()

        explanation = request.form.get(
            "explanation", ""
        ).strip()

        if not all([
            question_text,
            option_a,
            option_b,
            option_c,
            option_d,
            correct_answer
        ]):
            flash("All question fields are required.", "danger")
            return redirect(
                url_for("quiz.add_question", quiz_id=quiz_id)
            )

        if any(len(option) > 500 for option in [
            option_a, option_b, option_c, option_d
        ]):
            flash("Each option must be 500 characters or fewer.", "danger")
            return redirect(
                url_for("quiz.add_question", quiz_id=quiz_id)
            )

        if correct_answer not in ["A", "B", "C", "D"]:
            flash("Select a valid correct answer.", "danger")
            return redirect(
                url_for("quiz.add_question", quiz_id=quiz_id)
            )

        new_question = Question(
            quiz_id=quiz_id,
            question_text=question_text,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_answer=correct_answer,
            explanation=explanation or None
        )

        db.session.add(new_question)
        db.session.commit()

        flash("Question added successfully!", "success")

        return redirect(
            url_for("quiz.manage_questions", quiz_id=quiz_id)
        )

    return render_template(
        "admin/add_question.html",
        quiz=existing_quiz
    )


# --------------------------------
# ADMIN: EDIT QUESTION
# --------------------------------

@quiz.route(
    "/admin/questions/edit/<int:question_id>",
    methods=["GET", "POST"]
)
@admin_required
def edit_question(question_id):

    question = db.get_or_404(Question, question_id)

    if request.method == "POST":

        question_text = request.form.get(
            "question_text", ""
        ).strip()

        option_a = request.form.get("option_a", "").strip()
        option_b = request.form.get("option_b", "").strip()
        option_c = request.form.get("option_c", "").strip()
        option_d = request.form.get("option_d", "").strip()

        correct_answer = request.form.get(
            "correct_answer", ""
        ).strip().upper()

        explanation = request.form.get(
            "explanation", ""
        ).strip()

        if not all([
            question_text,
            option_a,
            option_b,
            option_c,
            option_d,
            correct_answer
        ]):
            flash("All question fields are required.", "danger")
            return redirect(
                url_for("quiz.edit_question", question_id=question_id)
            )

        if any(len(option) > 500 for option in [
            option_a, option_b, option_c, option_d
        ]):
            flash("Each option must be 500 characters or fewer.", "danger")
            return redirect(
                url_for("quiz.edit_question", question_id=question_id)
            )

        if correct_answer not in ["A", "B", "C", "D"]:
            flash("Select a valid correct answer.", "danger")
            return redirect(
                url_for("quiz.edit_question", question_id=question_id)
            )

        question.question_text = question_text
        question.option_a = option_a
        question.option_b = option_b
        question.option_c = option_c
        question.option_d = option_d
        question.correct_answer = correct_answer
        question.explanation = explanation or None

        db.session.commit()

        flash("Question updated successfully!", "success")

        return redirect(
            url_for(
                "quiz.manage_questions",
                quiz_id=question.quiz_id
            )
        )

    return render_template(
        "admin/edit_question.html",
        question=question
    )


# --------------------------------
# ADMIN: DELETE QUESTION
# --------------------------------

@quiz.route(
    "/admin/questions/delete/<int:question_id>",
    methods=["POST"]
)
@admin_required
def delete_question(question_id):

    question = db.get_or_404(Question, question_id)
    quiz_id = question.quiz_id

    db.session.delete(question)
    db.session.commit()

    flash("Question deleted successfully!", "success")

    return redirect(
        url_for("quiz.manage_questions", quiz_id=quiz_id)
    )

# --------------------------------
# USER: VIEW AVAILABLE ACTIVE QUIZZES
# --------------------------------

@quiz.route("/quizzes")
@login_required
def available_quizzes():

    available_quizzes = Quiz.query.filter_by(
        is_active=True
    ).order_by(
        Quiz.created_at.desc()
    ).all()

    return render_template(
        "quizzes.html",
        quizzes=available_quizzes
    )



# --------------------------------
# USER: ATTEMPT QUIZ
# --------------------------------

@quiz.route("/quizzes/<int:quiz_id>/attempt", methods=["GET", "POST"])
@login_required
def attempt_quiz(quiz_id):
    selected_quiz = Quiz.query.filter_by(
        id=quiz_id,
        is_active=True
    ).first_or_404()

    questions = Question.query.filter_by(
        quiz_id=selected_quiz.id
    ).order_by(Question.id.asc()).all()

    if not questions:
        flash("This quiz has no questions yet.", "warning")
        return redirect(url_for("quiz.available_quizzes"))

    if request.method == "POST":
        score = 0
        valid_options = {"A", "B", "C", "D"}
        submitted_answers = []

        for question in questions:
            user_answer = request.form.get(
                f"question_{question.id}", ""
            ).strip().upper()

            if user_answer not in valid_options:
                flash(
                    "Please answer all questions before submitting.",
                    "warning"
                )
                return redirect(url_for(
                    "quiz.attempt_quiz",
                    quiz_id=selected_quiz.id
                ))

            available_options = {
                "A": question.option_a,
                "B": question.option_b,
                "C": question.option_c,
                "D": question.option_d
            }

            if not available_options.get(user_answer):
                abort(400)

            is_correct = (
                user_answer == question.correct_answer.upper()
            )

            if is_correct:
                score += 1

            submitted_answers.append({
                "question_id": question.id,
                "selected_answer": user_answer,
                "is_correct": is_correct
            })

        total_questions = len(questions)
        percentage = round(
            (score / total_questions) * 100, 2
        )

        # Create quiz result
        result = QuizResult(
            user_id=current_user.id,
            quiz_id=selected_quiz.id,
            score=score,
            total_questions=total_questions,
            percentage=percentage
        )

        db.session.add(result)
        db.session.flush()

        # Save individual question answers
        for answer in submitted_answers:
            quiz_answer = QuizAnswer(
                result_id=result.id,
                question_id=answer["question_id"],
                selected_answer=answer["selected_answer"],
                is_correct=answer["is_correct"]
            )

            db.session.add(quiz_answer)

        db.session.commit()

        return redirect(url_for(
            "quiz.quiz_result",
            result_id=result.id
        ))

    return render_template(
        "quiz_attempt.html",
        quiz=selected_quiz,
        questions=questions
    )

# --------------------------------
# USER: VIEW QUIZ RESULT
# --------------------------------

@quiz.route("/quiz-results/<int:result_id>")
@login_required
def quiz_result(result_id):
    result = db.get_or_404(QuizResult, result_id)

    # Ensure users can only view their own results
    if result.user_id != current_user.id:
        abort(403)

    answer_reviews = []

    for answer in result.answers:
        question = answer.question

        options = {
            "A": question.option_a,
            "B": question.option_b,
            "C": question.option_c,
            "D": question.option_d
        }

        correct_letter = question.correct_answer.upper()

        answer_reviews.append({
            "question": question,
            "selected_letter": answer.selected_answer,
            "selected_text": options.get(
                answer.selected_answer, ""
            ),
            "correct_letter": correct_letter,
            "correct_text": options.get(
                correct_letter, ""
            ),
            "is_correct": answer.is_correct,
            "explanation": question.explanation
        })

    return render_template(
        "quiz_result.html",
        result=result,
        answer_reviews=answer_reviews
    )

# --------------------------------
# USER: VIEW QUIZ HISTORY
# --------------------------------

@quiz.route("/quiz-history")
@login_required
def quiz_history():

    user_results = QuizResult.query.filter_by(
        user_id=current_user.id
    ).order_by(
        QuizResult.completed_at.desc()
    ).all()

    # Performance Statistics
    total_attempts = len(user_results)

    if total_attempts > 0:
        best_score = max(
            result.percentage for result in user_results
        )

        average_score = sum(
            result.percentage for result in user_results
        ) / total_attempts
    else:
        best_score = 0
        average_score = 0



        # Quiz-wise Performance Tracking
    quiz_performance = {}

    for result in user_results:

        quiz_id = result.quiz_id

        if quiz_id not in quiz_performance:
            quiz_performance[quiz_id] = {
                "title": result.quiz.title,
                "category": result.quiz.category,
                "attempts": 0,
                "best_score": result.percentage,
                "total_score": 0,
                "latest_score": result.percentage,
                "latest_date": result.completed_at
            }

        stats = quiz_performance[quiz_id]

        stats["attempts"] += 1

        stats["total_score"] += result.percentage

        stats["best_score"] = max(
            stats["best_score"],
            result.percentage
        )

        if result.completed_at > stats["latest_date"]:
            stats["latest_score"] = result.percentage
            stats["latest_date"] = result.completed_at

    # Calculate average score for each quiz
    for stats in quiz_performance.values():

        stats["average_score"] = round(
            stats["total_score"] / stats["attempts"],
            2
        )

        stats["best_score"] = round(stats["best_score"], 2)


        return render_template(
        "quiz_history.html",
        results=user_results,
        total_attempts=total_attempts,
        best_score=round(best_score, 2),
        average_score=round(average_score, 2),
        quiz_performance=quiz_performance.values()
    )