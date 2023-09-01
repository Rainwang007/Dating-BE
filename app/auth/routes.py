from flask import Blueprint, request, jsonify, g, session
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError  # 需要安装email-validator包
import jwt
import datetime
import re
import logging
from models import db, User
import os
from dotenv import load_dotenv


load_dotenv()
auth = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)


@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # 用户名验证
    username = data.get('username', '').strip()
    if not username or len(username) < 3 or len(username) > 20:
        return jsonify({'error': 'Username must be between 3 and 20 characters'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    # 密码验证
    password = data.get('password', '')
    if len(password) < 8 or not re.search("[a-zA-Z]", password) or not re.search("[0-9]", password):
        return jsonify({'error': 'Password must be at least 8 characters, include letters and numbers'}), 400

    # 电子邮件验证（如果需要）
    email = data.get('email', '').strip()
    try:
        v = validate_email(email)
        email = v["email"]
    except EmailNotValidError as e:
        return jsonify({'error': str(e)}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400

    # 密码加密
    hashed_password = generate_password_hash(password, method='sha256')

    # 创建新用户
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Registered successfully'}), 201


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # 数据验证
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password are required'}), 400

    username = data['username']
    password = data['password']

    # 查找用户
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'Username does not exist'}), 401

    # 验证密码
    if not check_password_hash(user.password, password):
        return jsonify({'error': 'Password is incorrect'}), 401

    # 生成JWT
    token = jwt.encode({
    'user_id': 'some_user_id',
    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=10)
    }, os.getenv('JWT_SECRET_KEY'), algorithm='HS256')  # 请替换为你实际使用的密钥

    return jsonify({'token': token}), 200


def get_current_user():
    # 假设从Flask的session中获取当前用户ID
    user_id = session.get('user_id')
    # 在实际应用中，你可能需要从数据库或其他存储中获取用户对象
    return {'id': user_id, 'username': 'example_user'}

def clear_user_resources(user):
    # 在这里释放与用户相关的服务器资源
    # 例如，关闭数据库连接，清理缓存等
    pass

@auth.before_request
def pre_process():
    # 获取当前用户
    g.current_user = get_current_user()

@auth.route('/logout', methods=['GET'])
def logout():
    # 结束会话
    session.pop('user_id', None)

    # 记录登出行为
    logger.info(f"User {g.current_user['id']} logged out")

    # 清理资源
    clear_user_resources(g.current_user)

    return jsonify({'message': 'Logged out successfully'}), 200