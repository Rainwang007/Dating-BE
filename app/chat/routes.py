# routes.py
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity

chat_bp = Blueprint('chat', __name__)

# 假设的聊天数据存储（通常应从数据库获取）
chat_data = {
    'chat1': {'messages': []},
    'chat2': {'messages': []}
}

@chat_bp.route('/chats', methods=['GET'])
@jwt_required()
def get_chats():
    try:
        current_user = get_jwt_identity()
        # 实现获取聊天列表的逻辑，通常从数据库获取
        return jsonify({"chats": list(chat_data.keys())})
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@chat_bp.route('/chats/<chat_id>/messages', methods=['GET', 'POST'])
@jwt_required()
def manage_messages(chat_id):
    current_user = get_jwt_identity()

    if chat_id not in chat_data:
        return make_response(jsonify({"error": "Chat not found"}), 404)

    if request.method == 'GET':
        try:
            # 获取聊天记录
            messages = chat_data[chat_id]['messages']
            return jsonify({"messages": messages})
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

    elif request.method == 'POST':
        try:
            message_data = request.json
            message = {
                'user': current_user,
                'content': message_data['content']
            }
            # 实现发送消息的逻辑，通常存储消息到数据库
            chat_data[chat_id]['messages'].append(message)
            return jsonify({"message": "Message sent"})
        except KeyError:
            return make_response(jsonify({"error": "Content is required"}), 400)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)
