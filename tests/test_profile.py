import json
import pytest
from app import create_app
from models import Profile

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        yield client

def test_get_profile(client):
    # 模拟一个已登录的用户和获取个人资料的请求
    # 假设你有一个获取JWT令牌的方式
    token = "your_jwt_token_here"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.get('/profile/get', headers=headers)

    # 检查响应状态码和数据
    assert response.status_code == 200
    assert 'profile' in json.loads(response.data)

def test_update_profile(client):
    # 模拟一个已登录的用户和更新个人资料的请求
    # 假设你有一个获取JWT令牌的方式
    token = "your_jwt_token_here"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    updated_profile = {
        "age": 30,
        "bio": "New bio"
    }

    response = client.post('/profile/update', json=updated_profile, headers=headers)

    # 检查响应状态码和数据
    assert response.status_code == 200
    assert 'message' in json.loads(response.data)
    assert json.loads(response.data)['message'] == 'Profile updated successfully'


