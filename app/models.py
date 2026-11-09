from datetime import datetime, timezone
from flask_login import UserMixin
from app.extensions import db


def utc_now():
    return datetime.now(timezone.utc)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # Roles: user or admin
    role = db.Column(db.String(20), nullable=False, default="user")

    created_at = db.Column(db.DateTime(timezone=True), default=utc_now)

    quiz_results = db.relationship(
        "QuizResult",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class SecurityTip(db.Model):
    __tablename__ = "security_tips"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utc_now)


class Quiz(db.Model):
    __tablename__ = "quizzes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utc_now)

    questions = db.relationship(
        "Question",
        back_populates="quiz",
        cascade="all, delete-orphan"
    )

    results = db.relationship(
        "QuizResult",
        back_populates="quiz"
    )


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(
        db.Integer,
        db.ForeignKey("quizzes.id"),
        nullable=False
    )

    question_text = db.Column(db.Text, nullable=False)

    option_a = db.Column(db.String(500), nullable=False)
    option_b = db.Column(db.String(500), nullable=False)
    option_c = db.Column(db.String(500), nullable=False)
    option_d = db.Column(db.String(500), nullable=False)

    # Store only A, B, C or D as the correct answer
    correct_answer = db.Column(db.String(1), nullable=False)
    explanation = db.Column(db.Text)

    quiz = db.relationship("Quiz", back_populates="questions")


class QuizResult(db.Model):
    __tablename__ = "quiz_results"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    quiz_id = db.Column(
        db.Integer,
        db.ForeignKey("quizzes.id"),
        nullable=False
    )

    score = db.Column(db.Integer, nullable=False, default=0)
    total_questions = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False, default=0.0)

    completed_at = db.Column(db.DateTime(timezone=True), default=utc_now)

    user = db.relationship("User", back_populates="quiz_results")
    quiz = db.relationship("Quiz", back_populates="results")

    answers = db.relationship(
        "QuizAnswer",
        back_populates="result",
        cascade="all, delete-orphan"
    )


class QuizAnswer(db.Model):
    __tablename__ = "quiz_answers"

    id = db.Column(db.Integer, primary_key=True)

    result_id = db.Column(
        db.Integer,
        db.ForeignKey("quiz_results.id"),
        nullable=False
    )

    question_id = db.Column(
        db.Integer,
        db.ForeignKey("questions.id"),
        nullable=False
    )

    selected_answer = db.Column(db.String(1), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)

    result = db.relationship(
        "QuizResult",
        back_populates="answers"
    )

    question = db.relationship("Question")
