import pytest

from app import create_app, db
from app.models import User

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            yield client

@pytest.fixture
def login_test_user(client):
    email = 'john@test.com'
    password = 'password'
    User.create(
            firstname='John',
            lastname='Doe',
            email=email,
            password=password
            )
    login_response = client.post('/auth/login', json={
        'email': email,
        'password': password
        })
    json_login_response = login_response.get_json()
    return json_login_response['access_token']

