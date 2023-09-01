from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = '你的数据库连接字符串'

    jwt = JWTManager(app)

    from .auth.routes import auth_bp
    from .profile.routes import profile_bp
    from .match.routes import match_bp
    from .chat.routes import chat_bp
    
    db.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(match_bp)
    app.register_blueprint(chat_bp)

    return app
