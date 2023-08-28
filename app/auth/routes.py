# routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    user_data = request.json
    # 实现注册逻辑，如存储用户信息到数据库
    return jsonify({"message": "User registered"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    login_data = request.json
    username = login_data.get("username")
    password = login_data.get("password")
    # 实现登录逻辑，如验证用户名和密码
    access_token = create_access_token(identity=username)
    return jsonify({"access_token": access_token}), 200
