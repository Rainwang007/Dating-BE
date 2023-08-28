from flask import Flask
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')

    jwt = JWTManager(app)

    from .auth.routes import auth_bp
    from .profile.routes import profile_bp
    from .match.routes import match_bp
    from .chat.routes import chat_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(match_bp)
    app.register_blueprint(chat_bp)

    return app
