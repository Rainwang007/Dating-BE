import json
import pytest
from app import create_app
from models import Match

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        yield client

def test_get_matches(client):
    # 模拟一个已登录的用户和获取匹配列表的请求
    # 假设你有一个获取JWT令牌的方式
    token = "your_jwt_token_here"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.get('/match/list', headers=headers)

    # 检查响应状态码和数据
    assert response.status_code == 200
    assert 'matches' in json.loads(response.data)

def test_create_match(client):
    # 模拟一个已登录的用户和创建匹配的请求
    # 假设你有一个获取JWT令牌的方式
    token = "your_jwt_token_here"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    new_match = {
        "user_id_2": 2
    }

    response = client.post('/match/create', json=new_match, headers=headers)

    # 检查响应状态码和数据
    assert response.status_code == 201
    assert 'message' in json.loads(response.data)
    assert json.loads(response.data)['message'] == 'Match created successfully'


