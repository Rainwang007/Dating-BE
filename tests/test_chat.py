import json
import pytest
from app import create_app
from models import Chat

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        yield client

def test_get_chat_history(client):
    # 模拟一个已登录的用户和获取聊天历史的请求
    # 假设你有一个获取JWT令牌的方式
    token = "your_jwt_token_here"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.get('/chat/history', headers=headers)

    # 检查响应状态码和数据
    assert response.status_code == 200
    assert 'chat_history' in json.loads(response.data)

def test_send_message(client):
    # 模拟一个已登录的用户和发送消息的请求
    # 假设你有一个获取JWT令牌的方式
    token = "your_jwt_token_here"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    new_message = {
        "receiver_id": 2,
        "content": "Hello, how are you?"
    }

    response = client.post('/chat/send', json=new_message, headers=headers)

    # 检查响应状态码和数据
    assert response.status_code == 201
    assert 'message' in json.loads(response.data)
    assert json.loads(response.data)['message'] == 'Message sent successfully'

# 更多的测试函数...
