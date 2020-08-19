import pytest

from app import create_app
from .utils import client

def test_unauthorized_dashboard(client):
    response = client.get('/dashboard')
    json_response = response.get_json()
    assert json_response['msg'] == 'Missing Authorization Header'

def test_authorized_dashboard(client):
    login_response = client.post('/auth/login', json={
        'email': 'test@test.com',
        'password': 'password'
        })
    json_login_response = login_response.get_json()
    access_token = json_login_response['access_token']

    response = client.get('/dashboard', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()
    assert json_response["logged_in_as"] == 'test@test.com'

