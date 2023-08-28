# routes.py
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity

match_bp = Blueprint('match', __name__)

# 假设的匹配数据存储（通常应从数据库获取）
match_data = {
    'user1': {'likes': [], 'dislikes': []},
    'user2': {'likes': [], 'dislikes': []}
}

@match_bp.route('/matches', methods=['GET'])
@jwt_required()
def get_matches():
    try:
        current_user = get_jwt_identity()
        # 实现获取匹配列表的逻辑，通常从数据库获取
        return jsonify({"matches": list(match_data.keys())})
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@match_bp.route('/matches/<user_id>/like', methods=['POST'])
@jwt_required()
def like(user_id):
    try:
        current_user = get_jwt_identity()
        if user_id not in match_data:
            return make_response(jsonify({"error": "User not found"}), 404)
        
        # 实现喜欢逻辑，通常存储到数据库
        match_data[current_user]['likes'].append(user_id)
        return jsonify({"message": "Liked"})
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@match_bp.route('/matches/<user_id>/dislike', methods=['POST'])
@jwt_required()
def dislike(user_id):
    try:
        current_user = get_jwt_identity()
        if user_id not in match_data:
            return make_response(jsonify({"error": "User not found"}), 404)
        
        # 实现不喜欢逻辑，通常存储到数据库
        match_data[current_user]['dislikes'].append(user_id)
        return jsonify({"message": "Disliked"})
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
