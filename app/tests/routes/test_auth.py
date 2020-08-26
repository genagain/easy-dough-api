import pytest

from flask_bcrypt import generate_password_hash
from flask_jwt_extended import decode_token

from app import db
from app.models.user import User
from .utils import client

## TODO add a fixture to create this user before most of these tests
    # user = User(
            # firstname='Test',
            # lastname='User',
            # email='test@test.com',
            # password='password'
            # )
    # db.session.add(user)
    # db.session.commit()

def test_valid_signup(client):
    no_user =  User.query.filter_by(email='jane@test.com').first()
    assert no_user is None

    body = {
        'firstname': 'Jane',
        'lastname' : 'Test',
        'email': 'jane@test.com',
        'password': 'password'
        }
    response = client.post('/auth/signup', json=body)
    json_response = response.get_json()
    message = json_response['message']
    assert message == "Successfully created a new user"
    assert response.status_code == 200

    user =  User.query.filter_by(email='jane@test.com').first()
    assert user is not None
    assert user.firstname == body['firstname']
    assert user.lastname == body['lastname']
    assert user.email == body['email']
    assert user.password == body['password']

def test_duplicate_signup(client):
    user = User(
            firstname='Jerry',
            lastname='Test',
            email='jerry@test.com',
            password='password'
            )
    db.session.add(user)
    db.session.commit()

    body = {
        'firstname': 'Jerry',
        'lastname' : 'Doe',
        'email': 'jerry@test.com',
        'password': 'password'
        }

    response = client.post('/auth/signup', json=body)
    json_response = response.get_json()
    message = json_response['message']
    assert message == "A user with the email jerry@test.com already exists"
    assert response.status_code == 501

## TODO add format and body tests to signup

def test_valid_login(client):
    hashed_password = generate_password_hash('password').decode('utf-8')
    import pdb; pdb.set_trace()
    user = User(
            firstname='James',
            lastname='Test',
            email='james@test.com',
            password=hashed_password
            )
    db.session.add(user)
    db.session.commit()

    response = client.post('/auth/login', json={
        'email': 'james@test.com',
        'password': 'password'
        })
    json_response = response.get_json()
    access_token = json_response['access_token']
    decoded_token = decode_token(access_token)
    assert decoded_token['identity'] == 'james@test.com'
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
