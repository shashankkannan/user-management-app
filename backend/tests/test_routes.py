import pytest
import requests

BASE_URL = "http://localhost:7000"

def test_register():
    payload = {
	"username": "Shanky",
    "password": "12345678",
    "name": "Shashank Kannan",
    "email": "98shanky@gmail.com"
    }
    res = requests.post(f'{BASE_URL}/register', json=payload)
    assert res.status_code in (200, 400)

def test_login():
    payload = {
        "username": "Shanky",
        "password": "12345678"
    }
    res = requests.post(f'{BASE_URL}/login', json=payload)
    assert res.status_code == 200
    data = res.json()
    assert 'token' in data
    assert 'user_id' in data

def test_protected_get_users():
    payload = {
        "username": "Shanky",
        "password": "12345678"
    }
    login = requests.post(f'{BASE_URL}/login', json=payload)
    data = login.json()
    token = data['token']
    headers = {'Authorization': f'Bearer {token}'}
    res = requests.get(f'{BASE_URL}/users', headers=headers)
    print(res.json())
    assert res.status_code == 200

def test_update_user():
    payload = {
        "username": "Shanky",
        "password": "12345678"
    }
    login = requests.post(f'{BASE_URL}/login', json=payload)
    data = login.json()
    token = data['token']
    headers = {'Authorization': f'Bearer {token}'}
    id = data['user_id']
    payload_update = {
        'username': "Shankyman"
    }
    update = requests.put(f'{BASE_URL}/users/{id}', json=payload_update, headers=headers)
    assert update.status_code == 200
    assert update.json()['message'] == "User updated successfully"

def test_delete_user():
    payload = {
	"username": "temp",
    "password": "12345678",
    "name": "temp user",
    "email": "temp@gmail.com"
    }
    res = requests.post(f'{BASE_URL}/register', json=payload)

    login = requests.post(f'{BASE_URL}/login', json = {
        'username': "temp",
        "password": "12345678"
    }).json()
    token = login['token']
    id = login['user_id']

    headers = {'Authorization': f'Bearer {token}'}

    delete_user_res = requests.delete(f'{BASE_URL}/users/{id}', headers=headers)
    assert delete_user_res.status_code == 200
    assert delete_user_res.json()['message'] == "User deleted"

    