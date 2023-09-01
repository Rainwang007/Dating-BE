import json
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        yield client

def test_app_flow(client):
    # 测试用户注册
    new_user = {
        "username": "testuser",
        "password": "testpass"
    }
    register_response = client.post('/auth/register', json=new_user)
    assert register_response.status_code == 201
    assert b"Registration successful" in register_response.data

    # 测试用户登录
    user_credentials = {
        "username": "testuser",
        "password": "testpass"
    }
    login_response = client.post('/auth/login', json=user_credentials)
    assert login_response.status_code == 200
    login_data = json.loads(login_response.data)
    token = login_data.get("token")

    # 测试获取个人资料
    headers = {
        "Authorization": f"Bearer {token}"
    }
    get_profile_response = client.get('/profile/get', headers=headers)
    assert get_profile_response.status_code == 200
    assert 'profile' in json.loads(get_profile_response.data)

    # 测试更新个人资料
    updated_profile = {
        "age": 30,
        "bio": "New bio"
    }
    update_profile_response = client.post('/profile/update', json=updated_profile, headers=headers)
    assert update_profile_response.status_code == 200
    assert 'message' in json.loads(update_profile_response.data)
    assert json.loads(update_profile_response.data)['message'] == 'Profile updated successfully'
