from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, db 

profile = Blueprint('profile', __name__)

@profile.route('/api/profile', methods=['GET'])
@jwt_required()
def get_current_user_profile():
    current_user_id = get_jwt_identity()  # 使用JWT获取当前用户ID

    try:
        # 从数据库中获取当前用户的资料
        current_user = User.query.filter_by(id=current_user_id).first()

        if not current_user:
            return jsonify({'error': 'User not found'}), 404

        # 假设User模型有一个方法to_dict()，用于将用户资料转换为字典
        user_profile = current_user.to_dict()

        return jsonify({'profile': user_profile}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@profile.route('/api/profile', methods=['PUT'])
@jwt_required()
def update_current_user_profile():
    current_user_id = get_jwt_identity()  # 使用JWT获取当前用户ID
    data = request.json  # 获取请求的JSON数据

    try:
        # 从数据库中获取当前用户的资料
        current_user = User.query.filter_by(id=current_user_id).first()

        if not current_user:
            return jsonify({'error': 'User not found'}), 404

        # 更新用户资料
        if 'username' in data:
            current_user.username = data['username']
        if 'email' in data:
            current_user.email = data['email']
        if 'bio' in data:
            current_user.bio = data['bio']
        # ... 其他需要更新的字段

        db.session.commit()

        return jsonify({'message': 'Profile updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500