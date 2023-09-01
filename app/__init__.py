from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from dotenv import load_dotenv
from config import Config
from app.auth.routes import auth as auth_blueprint
from app.chat.routes import chat as chat_blueprint
from app.match.routes import match_bp as match_blueprint
from app.profile.routes import profile as profile_blueprint


load_dotenv()


# 初始化各种扩展
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # 数据库配置
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # JWT 配置
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'

    # 初始化各种扩展
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # CORS 配置
    CORS(app, resources={r"/api/*": {"origins": "your_domain.com"}})

    # 导入蓝图（Blueprints）
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(chat_blueprint)
    app.register_blueprint(match_blueprint)
    app.register_blueprint(profile_blueprint)

    with app.app_context():
         db.create_all()


    return app
