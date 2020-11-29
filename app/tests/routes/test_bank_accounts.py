import pytest

from app import db
from app.models import User, Bank, Account
from .utils import client, login_test_user

def test_unauthorized_bank_accounts(client):
    response = client.get('/bank_accounts')
    json_response = response.get_json()
    assert json_response['msg'] == 'Missing Authorization Header'

def test_no_bank_accounts(client, login_test_user):
    access_token = login_test_user

    response = client.get('/bank_accounts', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()
    assert json_response["message"] == 'No bank accounts have been added yet'
