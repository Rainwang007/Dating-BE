from flask import Blueprint, request, jsonify, g, session
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError  
import jwt
import datetime
import re
import logging
from models import db, User, Profile
import os
from dotenv import load_dotenv
import uuid


load_dotenv()
auth = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)


@auth.route('/api/register', methods=['POST'])
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
    generated_user_id = str(uuid.uuid4())
    new_user = User(user_id=generated_user_id, username=username, email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registered successfully'}), 201


@auth.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    # 数据验证
    if 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400

    email = data['email']
    password = data['password']

    # 查找用户
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'Email does not exist'}), 401

    # 验证密码
    if not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Password is incorrect'}), 401

    # 生成JWT
    token = jwt.encode({
        'sub': user.id,
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=10)
    }, os.getenv('JWT_SECRET_KEY'), algorithm='HS256')

    return jsonify({'token': token, 'message': 'Login successful'}), 200




def get_current_user():
    user_id = session.get('user_id')
    if user_id is not None:
        user = User.query.get(user_id)
        if user:
            return {'id': user.id, 'username': user.username, 'email': user.email}
    return None

def clear_user_resources(user):
    # placeholder for now
    pass

@auth.before_request
def pre_process():
    # 获取当前用户
    g.current_user = get_current_user()

@auth.route('/api/logout', methods=['GET'])
def logout():
    # 结束会话
    session.pop('user_id', None)

    # 记录登出行为
    logger.info(f"User {g.current_user['id']} logged out")

    # 清理资源
    clear_user_resources(g.current_user)

    return jsonify({'message': 'Logged out successfully'}), 200