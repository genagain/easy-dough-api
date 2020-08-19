import pytest

from app import create_app
from .utils import client

def test_unauthorized_dashboard(client):
    response = client.get('/dashboard')
    json_response = response.get_json()
    assert json_response['msg'] == 'Missing Authorization Header'
