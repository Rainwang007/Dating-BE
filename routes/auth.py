from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import create_user, check_user  # 假设你已经有了这些函数

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    user_data = request.json
    create_user(user_data)  # 存储用户到数据库
    return jsonify({"message": "User registered"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    login_data = request.json
    username = login_data.get("username")
    password = login_data.get("password")

    if not check_user(username, password):  # 验证用户
        return jsonify({"message": "Invalid username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify({"access_token": access_token}), 200
