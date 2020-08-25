import pytest

from flask_jwt_extended import decode_token

from app import db
from app.models.user import User
from .utils import client

def test_valid_signup(client):
    user = User(
            firstname='Test',
            lastname='User',
            email='test@test.com',
            password='password'
            )
    db.session.add(user)
    db.session.commit()

def test_valid_login(client):
    response = client.post('/auth/login', json={
        'email': 'test@test.com',
        'password': 'password'
        })
    json_response = response.get_json()
    access_token = json_response['access_token']
    decoded_token = decode_token(access_token)
    assert decoded_token['identity'] == 'test@test.com'
    assert response.status_code == 200

def test_invalid_login(client):
    response = client.post('/auth/login', json={
        'email': 'test@test.com',
        'password': 'bad password'
        })
    json_response = response.get_json()
    message = json_response['message']
    assert message == "Bad email or password"
    assert response.status_code == 401

def test_invalid_format(client):
    response = client.post('/auth/login', data={
        'email': 'test@test.com',
        'password': 'password'
        })
    json_response = response.get_json()
    message = json_response['message']
    assert message == "Invalid format: body must be JSON"
    assert response.status_code == 501

def test_invalid_body(client):
    for attribute in ['email', 'password']:
        invalid_body = { attribute: 'something' }
        response = client.post('/auth/login', json=invalid_body)
        json_response = response.get_json()
        message = json_response['message']
        assert message == "Invalid body: body must contain email and password"
        assert response.status_code == 501
