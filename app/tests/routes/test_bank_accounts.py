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

def test_one_bank_two_accounts(client, login_test_user):
    access_token = login_test_user
    user = User.query.filter_by(email="john@test.com").first()

    ally_logo = "fake ally logo"
    bank = Bank(name='Ally', access_token='fake access token', logo=ally_logo, user=user)
    checking_account = Account(name="Expenses", plaid_account_id="fake account id", type="checking", bank=bank)
    savings_account = Account(name="Savings Account", plaid_account_id="another fake account id", type="savings", bank=bank)
    db.session.add(bank)
    db.session.add(checking_account)
    db.session.add(savings_account)
    db.session.commit()

    response = client.get('/bank_accounts', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()

    assert json_response == {
            'banks': [
                    {
                        'id': 1,
                        'name': 'Ally',
                        'logo': ally_logo,
                        'accounts': [
                            {
                                'name':'Expenses',
                                'type': 'Checking'
                            },
                            {
                                'name':'Savings Account',
                                'type': 'Savings'
                            }
                        ]
                    }
                ]
            }


def test_valid_bank_delete(client, login_test_user):
    access_token = login_test_user
    user = User.query.filter_by(email="john@test.com").first()

    ally_logo = "fake ally logo"
    bank = Bank(name='Ally Bank', access_token='fake access token', logo=ally_logo, user=user)
    checking_account = Account(name="Expenses", plaid_account_id="fake account id", type="checking", bank=bank)
    savings_account = Account(name="Savings Account", plaid_account_id="another fake account id", type="savings", bank=bank)
    db.session.add(bank)
    db.session.add(checking_account)
    db.session.add(savings_account)
    db.session.commit()

    response = client.delete('/bank_accounts/1', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()
    assert json_response["message"] == 'Bank Accounts successfully deleted'

    deleted_bank = Bank.query.filter_by(name='Ally Bank', user=user).first()
    assert deleted_bank == None

    deleted_account_1 = Account.query.filter_by(plaid_account_id="fake account id").first()
    assert deleted_account_1 == None

    deleted_account_2 = Account.query.filter_by(plaid_account_id="another fake account id").first()
    assert deleted_account_2 == None

def test_invalid_bank_delete(client, login_test_user):
    access_token = login_test_user

    response = client.delete('/bank_accounts/1', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()
    assert json_response["message"] == 'Cannot delete these bank accounts because they do not exist'
    assert response.status_code == 501
