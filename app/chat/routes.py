
from flask import Blueprint, request, jsonify, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import  Match, User, db


chat = Blueprint('chat', __name__)

@chat.route('/api/get_email', methods=['GET'])
@jwt_required()
def get_email():
    current_user_id = get_jwt_identity()
    matched_users = {}

    # 找到所有满足条件的匹配
    matches1 = Match.query.filter_by(user1_id=current_user_id, status='liked').all()
    matches2 = Match.query.filter_by(user2_id=current_user_id, status='liked').all()

    for match in matches1:
        corresponding_match = Match.query.filter_by(user1_id=match.user2_id, user2_id=current_user_id, status='liked').first()
        if corresponding_match:
            user = User.query.filter_by(id=match.user2_id).first()
            if user:
                matched_users[user.id] = {'username': user.username, 'email': user.email}

    for match in matches2:
        corresponding_match = Match.query.filter_by(user1_id=match.user1_id, user2_id=current_user_id, status='liked').first()
        if corresponding_match:
            user = User.query.filter_by(id=match.user1_id).first()
            if user:
                matched_users[user.id] = {'username': user.username, 'email': user.email}

    return jsonify({'matched_users': matched_users})


