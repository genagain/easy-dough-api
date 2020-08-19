import pytest

from app import create_app
from .utils import client

def test_root(client):
    response = client.get('/dashboard')
    assert b'msg' in response.data
    assert b'Missing Authorization Header' in response.data
