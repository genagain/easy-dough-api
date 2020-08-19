import pytest

from app import create_app
from flask_jwt_extended import decode_token

## TODO put this in test utils
@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
      yield client

def test_root(client):
    response = client.post('/auth/login', json={
        'email': 'test@test.com',
        'password': 'password'
        })
    json_response = response.get_json()
    access_token = json_response['access_token']
    decoded_token = decode_token(access_token)
    assert decoded_token['identity'] == 'test@test.com'

