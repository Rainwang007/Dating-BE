from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Profile, Match, db
from random import choice

match = Blueprint('match', __name__) 

@match.route('/api/matches/random', methods=['GET'])
@jwt_required()
def get_random_match():
    current_user_id = get_jwt_identity()
    try:
        all_profiles = Profile.query.filter(Profile.user_id != current_user_id).all()
        if not all_profiles:
            return jsonify({'error': 'No profiles available for matching'}), 404
        random_profile = choice(all_profiles)
        random_profile_data = {
            'name': random_profile.name,
            'age': random_profile.age,
            'location': random_profile.location,
            'bio': random_profile.bio,
            'avatar_url': random_profile.avatar_url,
            'user_id': random_profile.user_id  # 添加这一行
        }


        return jsonify({'match': random_profile_data}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@match.route('/api/matches/<string:target_user_id>/like', methods=['POST'])
@jwt_required()
def like_user(target_user_id):
    current_user_id = get_jwt_identity()
    target_user = Profile.query.filter_by(user_id=target_user_id).first_or_404(description='Target user not found')

    try:
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


@match.route('/api/matches/<int:target_user_id>/dislike', methods=['POST'])
@jwt_required()
def dislike_user(target_user_id):
    current_user_id = get_jwt_identity()
    target_user = User.query.filter_by(id=target_user_id).first_or_404(description='Target user not found')

    try:
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