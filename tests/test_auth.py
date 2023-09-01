import json
import pytest
from app import create_app
from models import User

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        yield client

def test_register(client):
    # 准备测试数据
    new_user = {
        "username": "testuser",
        "password": "testpass"
    }

    # 发送POST请求
    response = client.post('/auth/register', json=new_user)

    # 检查响应状态码和数据
    assert response.status_code == 201
    assert b"Registration successful" in response.data

def test_login(client, mock_jwt):
    # 准备测试数据
    user_credentials = {
        "username": "existinguser",
        "password": "existingpass"
    }

    # 发送POST请求
    response = client.post('/auth/login', json=user_credentials)

    # 检查响应状态码和数据
    assert response.status_code == 200
    assert b"Login successful" in response.data

    # 从响应中获取模拟的JWT令牌
    login_data = json.loads(response.data)
    token = login_data.get("token")

    assert token == "mocked_token"  # 确保使用了模拟的令牌


def test_logout(client):
    # 首先，模拟一个已登录的用户
    user_credentials = {
        "username": "existinguser",
        "password": "existingpass"
    }
    login_response = client.post('/auth/login', json=user_credentials)
    assert login_response.status_code == 200
    
    # 从登录响应中获取JWT令牌
    login_data = json.loads(login_response.data)
    token = login_data.get("token")
    
    # 使用JWT令牌发送登出请求
    headers = {
        "Authorization": f"Bearer {token}"
    }
    logout_response = client.post('/auth/logout', headers=headers)
    
    # 检查响应状态码和数据
    assert logout_response.status_code == 200
    assert b"Logout successful" in logout_response.data

