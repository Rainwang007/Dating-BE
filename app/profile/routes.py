# routes.py
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity

profile_bp = Blueprint('profile', __name__)

# 假设的用户资料数据存储（通常应从数据库获取）
profile_data = {
    'user1': {'name': 'Alice', 'age': 25, 'bio': 'Hello there!'},
    'user2': {'name': 'Bob', 'age': 30, 'bio': 'Nice to meet you!'}
}

@profile_bp.route('/profile', methods=['GET', 'PUT'])
@jwt_required()
def manage_profile():
    try:
        current_user = get_jwt_identity()
        if current_user not in profile_data:
            return make_response(jsonify({"error": "User not found"}), 404)

        if request.method == 'GET':
            # 获取用户资料
            return jsonify({"profile": profile_data[current_user]})

        elif request.method == 'PUT':
            # 更新用户资料
            updated_data = request.json
            profile_data[current_user].update(updated_data)
            return jsonify({"message": "Profile updated"})

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
