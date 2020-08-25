import pytest

from flask_jwt_extended import decode_token

from .utils import client

def test_valid_login(client):
    response = client.post('/auth/login', json={
        'email': 'test@test.com',
        'password': 'password'
        })
    json_response = response.get_json()
    access_token = json_response['access_token']
    decoded_token = decode_token(access_token)
    assert decoded_token['identity'] == 'test@test.com'

def test_invalid_login(client):
    response = client.post('/auth/login', json={
        'email': 'test@test.com',
        'password': 'bad password'
        })
    json_response = response.get_json()
    message = json_response['message']
    assert message == "Bad email or password"
