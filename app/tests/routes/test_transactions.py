import pytest

from flask_bcrypt import generate_password_hash
from app import db
from app.models import User
from .utils import client

def test_unauthorized_transactions(client):
    response = client.get('/transactions')
    json_response = response.get_json()
    assert json_response['msg'] == 'Missing Authorization Header'

def test_authorized_transactions(client):
    hashed_password = generate_password_hash('password').decode('utf-8')
    user = User(
            firstname='Jessica',
            lastname='Test',
            email='jessica@test.com',
            password=hashed_password
            )
    db.session.add(user)
    db.session.commit()

    login_response = client.post('/auth/login', json={
        'email': 'jessica@test.com',
        'password': 'password'
        })
    json_login_response = login_response.get_json()
    access_token = json_login_response['access_token']

    response = client.get('/transactions', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()
    assert json_response["logged_in_as"] == 'jessica@test.com'

