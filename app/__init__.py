from flask import Flask
from config import Config
from app.extensions import db, login_manager, csrf


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Load user for Flask-Login
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register blueprints
    from app.routes.main import main
    from app.routes.auth import auth
    from app.routes.tools import tools
    from app.routes.tips import tips
    from app.routes.quiz import quiz

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(tools)
    app.register_blueprint(tips)
    app.register_blueprint(quiz)

    return app