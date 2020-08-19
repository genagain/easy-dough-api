import pytest

from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_root(client):
    response = client.get('/dashboard')
    assert b'msg' in response.data
    assert b'Missing Authorization Header' in response.data
