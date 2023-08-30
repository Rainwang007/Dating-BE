
from flask import Blueprint, request, jsonify, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Chat, db

chat = Blueprint('chat', __name__)

@chat.route('/api/chat', methods=['GET'])
@jwt_required()
def get_chat_history():
    current_user_id = get_jwt_identity()  # 使用JWT获取当前用户ID
    target_user_id = request.args.get('target_user_id')  # 从请求参数中获取目标用户ID

    if not target_user_id:
        return jsonify({'error': 'Target user ID is required'}), 400

    # 假设Chat模型有一个类方法get_chat_history来获取聊天记录
    chat_history = Chat.get_chat_history(current_user_id, target_user_id)

    if not chat_history:
        return jsonify({'error': 'No chat history found'}), 404

    return jsonify({'chat_history': chat_history}), 200

@chat.route('/api/chat', methods=['POST'])
@jwt_required()
def send_message():
    current_user_id = get_jwt_identity()  # 使用JWT获取当前用户ID
    data = request.json  # 获取请求的JSON数据

    target_user_id = data.get('target_user_id')
    message_content = data.get('message')

    if not target_user_id or not message_content:
        return jsonify({'error': 'Target user ID and message content are required'}), 400

    try:
        # 创建新的Chat对象并保存到数据库
        new_message = Chat(sender_id=current_user_id, receiver_id=target_user_id, content=message_content)
        db.session.add(new_message)
        db.session.commit()

        return jsonify({'message': 'Message sent successfully'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
