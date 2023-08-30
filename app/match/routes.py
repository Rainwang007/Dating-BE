from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Match, db

match_bp = Blueprint('match', __name__)

matches = Blueprint('matches', __name__)

@matches.route('/api/matches', methods=['GET'])
@jwt_required()
def get_current_user_matches():
    current_user_id = get_jwt_identity()  # 使用JWT获取当前用户ID

    try:
        # 从数据库中获取当前用户的所有匹配
        current_user = User.query.filter_by(id=current_user_id).first()

        if not current_user:
            return jsonify({'error': 'User not found'}), 404

        # 假设Match模型有一个方法get_matches(user_id)，用于获取用户的所有匹配
        user_matches = Match.get_matches(current_user_id)

        # 将匹配列表转换为字典列表
        matches_list = [match.to_dict() for match in user_matches]

        return jsonify({'matches': matches_list}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@matches.route('/api/matches/<int:target_user_id>/like', methods=['POST'])
@jwt_required()
def like_user(target_user_id):
    current_user_id = get_jwt_identity()  # 使用JWT获取当前用户ID

    try:
        # 检查目标用户是否存在
        target_user = User.query.filter_by(id=target_user_id).first()
        if not target_user:
            return jsonify({'error': 'Target user not found'}), 404

        # 检查当前用户是否已经喜欢过目标用户
        existing_match = Match.query.filter_by(user_id=current_user_id, target_user_id=target_user_id).first()
        if existing_match:
            return jsonify({'error': 'Already liked this user'}), 400

        # 创建新的匹配记录
        new_match = Match(user_id=current_user_id, target_user_id=target_user_id, status='liked')
        db.session.add(new_match)
        db.session.commit()

        return jsonify({'message': 'Successfully liked the user'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
    
@matches.route('/matches/<int:target_user_id>/dislike', methods=['POST'])
@jwt_required()
def dislike_user(target_user_id):
    current_user_id = get_jwt_identity()  # 使用JWT获取当前用户ID

    try:
        # 检查目标用户是否存在
        target_user = User.query.filter_by(id=target_user_id).first()
        if not target_user:
            return jsonify({'error': 'Target user not found'}), 404

        # 检查当前用户是否已经对目标用户表示过不喜欢
        existing_match = Match.query.filter_by(user_id=current_user_id, target_user_id=target_user_id).first()
        if existing_match:
            return jsonify({'error': 'Already disliked this user'}), 400

        # 创建新的匹配记录，标记为不喜欢
        new_match = Match(user_id=current_user_id, target_user_id=target_user_id, status='disliked')
        db.session.add(new_match)
        db.session.commit()

        return jsonify({'message': 'Successfully disliked the user'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500