import pytest

from flask_bcrypt import check_password_hash, generate_password_hash
from flask_jwt_extended import decode_token

from app import db
from app.models import User
from .utils import client

## TODO add a fixture to create this user before most of these tests
    # user = User(
            # firstname='Doe',
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
        'firstname': 'John',
        'lastname' : 'Doe',
        'email': 'john@test.com',
        'password': 'password'
        }
    response = client.post('/auth/signup', json=body)
    json_response = response.get_json()
    message = json_response['message']
    assert message == "Successfully created a new user"
    assert response.status_code == 200

    user =  User.query.filter_by(email='john@test.com').first()
    assert user is not None
    assert user.firstname == body['firstname']
    assert user.lastname == body['lastname']
    assert user.email == body['email']
    assert check_password_hash(user.password, body['password'])

def test_duplicate_signup(client):
    User.create(
            firstname='John',
            lastname='Doe',
            email='john@test.com',
            password='password'
            )

    body = {
        'firstname': 'John',
        'lastname' : 'Doe',
        'email': 'john@test.com',
        'password': 'password'
        }

    response = client.post('/auth/signup', json=body)
    json_response = response.get_json()
    message = json_response['message']
    assert message == "A user with the email john@test.com already exists"
    assert response.status_code == 501

def test_invalid_format_signup(client):
    body = {
        'firstname': 'John',
        'lastname' : 'Doe',
        'email': 'john@test.com',
        'password': 'password'
        }
    response = client.post('/auth/signup', data=body)
    json_response = response.get_json()
    message = json_response['message']
    assert message == "Invalid format: body must be JSON"
    assert response.status_code == 501


def test_invalid_body_signup(client):
    for attribute in ['firstname', 'lastname', 'email', 'password']:
        invalid_body = {
            'firstname': 'John',
            'lastname' : 'Doe',
            'email': 'john@test.com',
            'password': 'password'
        }
        invalid_body.pop(attribute)
        response = client.post('/auth/signup', json=invalid_body)
        json_response = response.get_json()
        message = json_response['message']
        assert message == "Invalid body: body must contain firstname, lastname, email and password"
        assert response.status_code == 501

def test_valid_login(client):
    User.create(
            firstname='John',
            lastname='Doe',
            email='john@test.com',
            password='password'
            )

    response = client.post('/auth/login', json={
        'email': 'john@test.com',
        'password': 'password'
        })
    json_response = response.get_json()
    access_token = json_response['access_token']
    decoded_token = decode_token(access_token)
    assert decoded_token['identity'] == 'john@test.com'
    assert response.status_code == 200

def test_invalid_login(client):
    User.create(
            firstname='John',
            lastname='Doe',
            email='john@test.com',
            password='password'
            )

    response = client.post('/auth/login', json={
        'email': 'john@test.com',
        'password': 'bad password'
        })
    json_response = response.get_json()
    message = json_response['message']
    assert message == "Bad email or password"
    assert response.status_code == 401

def test_invalid_format_login(client):
    response = client.post('/auth/login', data={
        'email': 'john@test.com',
        'password': 'password'
        })
    json_response = response.get_json()
    message = json_response['message']
    assert message == "Invalid format: body must be JSON"
    assert response.status_code == 501

def test_invalid_body_login(client):
    for attribute in ['email', 'password']:
        invalid_body = { attribute: 'something' }
        response = client.post('/auth/login', json=invalid_body)
        json_response = response.get_json()
        message = json_response['message']
        assert message == "Invalid body: body must contain email and password"
        assert response.status_code == 501
