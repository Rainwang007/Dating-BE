from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Profile, db

profile = Blueprint('profile', __name__)

@profile.route('/api/profile', methods=['GET'])
@jwt_required()
def get_current_user_profile():
    current_user_id = get_jwt_identity()
    try:
        current_profile = Profile.query.filter_by(user_id=current_user_id).first()
        if not current_profile:
            return jsonify({'error': 'Profile not found'}), 404
        profile_data = {
            'name': current_profile.name,
            'age': current_profile.age,
            'location': current_profile.location,
            'bio': current_profile.bio,
            'avatar_url': current_profile.avatar_url
        }
        return jsonify({'profile': profile_data}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@profile.route('/api/profile', methods=['PUT'])
@jwt_required()
def update_current_user_profile():
    current_user_id = get_jwt_identity()
    data = request.json
    try:
        current_profile = Profile.query.filter_by(user_id=current_user_id).first()

        # 如果Profile不存在，创建一个新的
        if not current_profile:
            current_profile = Profile(user_id=current_user_id)
            db.session.add(current_profile)

        if 'name' in data:
            current_profile.name = data['name']
        if 'age' in data:
            current_profile.age = data['age']
        if 'location' in data:
            current_profile.location = data['location']
        if 'bio' in data:
            current_profile.bio = data['bio']
        if 'avatar_url' in data:
            current_profile.avatar_url = data['avatar_url']

        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

