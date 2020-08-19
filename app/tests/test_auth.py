import pytest

from app import create_app
from flask_jwt_extended import decode_token

from .utils import client

def test_login(client):
    response = client.post('/auth/login', json={
        'email': 'test@test.com',
        'password': 'password'
        })
    json_response = response.get_json()
    access_token = json_response['access_token']
    decoded_token = decode_token(access_token)
    assert decoded_token['identity'] == 'test@test.com'

