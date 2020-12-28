from datetime import date
import pytest

from app import db
from app.models import User, Bank, Account, Transaction, SpendingPlanPart
from .utils import client, login_test_user

def test_unauthorized_transactions(client):
    response = client.get('/transactions')
    json_response = response.get_json()
    assert json_response['msg'] == 'Missing Authorization Header'

def test_transactions_no_query_params(client, login_test_user):
    access_token = login_test_user

    response = client.get('/transactions', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()
    assert json_response["message"] == 'Query parameters not found. Please provide both a start date and end date and optionally a search term in the request'


def test_transactions_invalid_query_params(client, login_test_user):
    access_token = login_test_user

    response = client.get('/transactions?something=invalid', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()
    assert json_response["message"] == 'Query parameters not found. Please provide both a start date and end date and optionally a search term in the request'

def test_transactions_one_month_one_transaction_two_users(client, login_test_user):
    other_user = User.create(firstname='Jane', lastname='', email='jane@test.com', password='test_password')
    other_bank = Bank(
            name='Ally Bank',
            access_token='other fake access token',
            logo='other fake logo',
            user=other_user
            )
    other_account = Account(
            plaid_account_id='other fake account id',
            name='Checking Account',
            type='checking',
            bank=other_bank
            )
    db.session.add(other_bank)
    db.session.add(other_account)
    db.session.commit()

    access_token = login_test_user

    user = User.query.filter_by(email='john@test.com').first()

    bank = Bank(
            name='Ally Bank',
            access_token='fake access token',
            logo='fake logo',
            user=user
            )
    account = Account(
            plaid_account_id='fake account id',
            name='Checking Account',
            type='checking',
            bank=bank
            )
    db.session.add(bank)
    db.session.add(account)
    db.session.commit()

    may_transaction = Transaction(date='2020-05-15', description='Mexican place', amount=1500, account=account)
    june_transaction = Transaction(date='2020-06-21', description='Italian restaurant', amount=2700, account=account)
    july_transaction = Transaction(date='2020-07-04', description='BBQ', amount=4000, account=account)

    db.session.add(may_transaction)
    db.session.add(june_transaction)
    db.session.add(july_transaction)
    db.session.commit()

    other_may_transaction = Transaction(date='2020-05-15', description='Mexican place', amount=1500, account=other_account)
    other_june_transaction = Transaction(date='2020-06-21', description='Italian restaurant', amount=2700, account=other_account)
    other_july_transaction = Transaction(date='2020-07-04', description='BBQ', amount=4000, account=other_account)

    db.session.add(other_may_transaction)
    db.session.add(other_june_transaction)
    db.session.add(other_july_transaction)
    db.session.commit()

    response = client.get('/transactions?start_date=2020-06-01&end_date=2020-06-30', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()

    expected_month = 'June'
    expected_transactions = [ { 'id': 2, 'date': '2020-06-21', 'description': 'Italian restaurant', 'amount': '27.00' } ]

    response_month = json_response[0]
    assert response_month['month'] == expected_month
    assert response_month['transactions'] == expected_transactions


def test_transactions_one_month_one_transaction(client, login_test_user):
    access_token = login_test_user

    user = User.query.filter_by(email='john@test.com').first()

    bank = Bank(
            name='Ally Bank',
            access_token='fake access token',
            logo='fake logo',
            user=user
            )
    account = Account(
            plaid_account_id='fake account id',
            name='Checking Account',
            type='checking',
            bank=bank
            )
    db.session.add(bank)
    db.session.add(account)
    db.session.commit()

    may_transaction = Transaction(date='2020-05-15', description='Mexican place', amount=1500, account=account)
    june_transaction = Transaction(date='2020-06-21', description='Italian restaurant', amount=2700, account=account)
    july_transaction = Transaction(date='2020-07-04', description='BBQ', amount=4000, account=account)

    db.session.add(may_transaction)
    db.session.add(june_transaction)
    db.session.add(july_transaction)
    db.session.commit()


    response = client.get('/transactions?start_date=2020-06-01&end_date=2020-06-30', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()

    expected_month = 'June'
    expected_transactions = [ { 'id': 2, 'date': '2020-06-21', 'description': 'Italian restaurant', 'amount': '27.00' } ]

    response_month = json_response[0]
    assert response_month['month'] == expected_month
    assert response_month['transactions'] == expected_transactions


def test_transactions_one_month_two_transactions(client, login_test_user):
    access_token = login_test_user

    user = User.query.filter_by(email='john@test.com').first()

    bank = Bank(
            name='Ally Bank',
            access_token='fake access token',
            logo='fake logo',
            user=user
            )
    account = Account(
            plaid_account_id='fake account id',
            name='Checking Account',
            type='checking',
            bank=bank
            )
    db.session.add(bank)
    db.session.add(account)
    db.session.commit()


    may_transaction = Transaction(date='2020-05-15', description='Mexican place', amount=1500, account=account)
    june_transaction_one = Transaction(date='2020-06-09', description='Japanese restaurant', amount=2300, account=account)
    june_transaction_two = Transaction(date='2020-06-21', description='Italian restaurant', amount=2700, account=account)
    july_transaction = Transaction(date='2020-07-04', description='BBQ', amount=4000, account=account)

    db.session.add(may_transaction)
    db.session.add(june_transaction_one)
    db.session.add(june_transaction_two)
    db.session.add(july_transaction)
    db.session.commit()

    response = client.get('/transactions?start_date=2020-06-01&end_date=2020-06-30', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()

    expected_month = 'June'
    expected_transactions = [
            { 'id': 3, 'date': '2020-06-21', 'description': 'Italian restaurant', 'amount': '27.00' },
            { 'id': 2, 'date': '2020-06-09', 'description': 'Japanese restaurant', 'amount': '23.00' }
            ]

    response_month = json_response[0]
    assert response_month['month'] == expected_month
    assert response_month['transactions'] == expected_transactions

def test_transactions_one_month_not_found(client, login_test_user):
    access_token = login_test_user

    user = User.query.filter_by(email='john@test.com').first()

    bank = Bank(
            name='Ally Bank',
            access_token='fake access token',
            logo='fake logo',
            user=user
            )
    account = Account(
            plaid_account_id='fake account id',
            name='Checking Account',
            type='checking',
            bank=bank
            )
    db.session.add(bank)
    db.session.add(account)
    db.session.commit()

    may_transaction = Transaction(date='2020-05-15', description='Mexican place', amount=1500, account=account)
    june_transaction_one = Transaction(date='2020-06-09', description='Japanese restaurant', amount=2300, account=account)
    june_transaction_two = Transaction(date='2020-06-21', description='Italian restaurant', amount=2700, account=account)
    july_transaction = Transaction(date='2020-07-04', description='BBQ', amount=4000, account=account)

    db.session.add(may_transaction)
    db.session.add(june_transaction_one)
    db.session.add(june_transaction_two)
    db.session.add(july_transaction)
    db.session.commit()

    response = client.get('/transactions?start_date=2020-01-01&end_date=2020-01-31', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()

    assert json_response == []


def test_transactions_no_start_date(client, login_test_user):
    access_token = login_test_user

    user = User.query.filter_by(email='john@test.com').first()

    bank = Bank(
            name='Ally Bank',
            access_token='fake access token',
            logo='fake logo',
            user=user
            )
    account = Account(
            plaid_account_id='fake account id',
            name='Checking Account',
            type='checking',
            bank=bank
            )
    db.session.add(bank)
    db.session.add(account)
    db.session.commit()

    may_transaction = Transaction(date='2020-05-15', description='Mexican place', amount=1500, account=account)
    june_transaction = Transaction(date='2020-06-21', description='Italian restaurant', amount=2700, account=account)
    july_transaction = Transaction(date='2020-07-04', description='BBQ', amount=4000, account=account)

    db.session.add(may_transaction)
    db.session.add(june_transaction)
    db.session.add(july_transaction)
    db.session.commit()

    response = client.get('/transactions?end_date=2020-06-30', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()

    assert 'start_date and end_date query parameters not found. Please provide both a start date and end date' == json_response['message']


def test_transactions_no_end_date(client, login_test_user):
    access_token = login_test_user

    user = User.query.filter_by(email='john@test.com').first()

    bank = Bank(
            name='Ally Bank',
            access_token='fake access token',
            logo='fake logo',
            user=user
            )
    account = Account(
            plaid_account_id='fake account id',
            name='Checking Account',
            type='checking',
            bank=bank
            )
    db.session.add(bank)
    db.session.add(account)
    db.session.commit()

    may_transaction = Transaction(date='2020-05-15', description='Mexican place', amount=1500, account=account)
    june_transaction = Transaction(date='2020-06-21', description='Italian restaurant', amount=2700, account=account)
    july_transaction = Transaction(date='2020-07-04', description='BBQ', amount=4000, account=account)

    db.session.add(may_transaction)
    db.session.add(june_transaction)
    db.session.add(july_transaction)
    db.session.commit()

    response = client.get('/transactions?start_date=2020-06-30', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()

    assert 'start_date and end_date query parameters not found. Please provide both a start date and end date' == json_response['message']

def test_transactions_search_term_found_one_transaction_two_users(client, login_test_user):
    other_user = User.create(firstname='Jane', lastname='', email='jane@test.com', password='test_password')
    other_bank = Bank(
            name='Ally Bank',
            access_token='other fake access token',
            logo='other fake logo',
            user=other_user
            )
    other_account = Account(
            plaid_account_id='other fake account id',
            name='Checking Account',
            type='checking',
            bank=other_bank
            )
    db.session.add(other_bank)
    db.session.add(other_account)
    db.session.commit()

    access_token = login_test_user

    user = User.query.filter_by(email='john@test.com').first()

    bank = Bank(
            name='Ally Bank',
            access_token='fake access token',
            logo='fake logo',
            user=user
            )
    account = Account(
            plaid_account_id='fake account id',
            name='Checking Account',
            type='checking',
            bank=bank
            )
    db.session.add(bank)
    db.session.add(account)
    db.session.commit()

    may_transaction = Transaction(date='2020-05-15', description='Mexican place', amount=1500, account=account)
    june_transaction = Transaction(date='2020-06-21', description='Italian restaurant', amount=2700, account=account)
    july_not_found_transaction = Transaction(date='2020-07-04', description='BBQ', amount=4000, account=account)
    july_found_transaction = Transaction(date='2020-07-21', description='Pizza Delivery', amount=2000, account=account)

    db.session.add(may_transaction)
    db.session.add(june_transaction)
    db.session.add(july_not_found_transaction)
    db.session.add(july_found_transaction)
    db.session.commit()

    other_may_transaction = Transaction(date='2020-05-15', description='Mexican place', amount=1500, account=other_account)
    other_june_transaction = Transaction(date='2020-06-21', description='Italian restaurant', amount=2700, account=other_account)
    other_july_not_found_transaction = Transaction(date='2020-07-04', description='BBQ', amount=4000, account=other_account)
    other_july_found_transaction = Transaction(date='2020-07-21', description='Pizza Delivery', amount=2000, account=other_account)

    db.session.add(other_may_transaction)
    db.session.add(other_june_transaction)
    db.session.add(other_july_not_found_transaction)
    db.session.add(other_july_found_transaction)
    db.session.commit()

    response = client.get('/transactions?start_date=2020-07-01&end_date=2020-07-31&search_term=pizza+del', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()

    expected_month = 'July'
    expected_transactions = [ { 'id': 4, 'date': '2020-07-21', 'description': 'Pizza Delivery', 'amount': '20.00' } ]

    response_month = json_response[0]
    assert response_month['month'] == expected_month
    assert response_month['transactions'] == expected_transactions


def test_transactions_search_term_found_one_transaction(client, login_test_user):
    access_token = login_test_user

    user = User.query.filter_by(email='john@test.com').first()

    bank = Bank(
            name='Ally Bank',
            access_token='fake access token',
            logo='fake logo',
            user=user
            )
    account = Account(
            plaid_account_id='fake account id',
            name='Checking Account',
            type='checking',
            bank=bank
            )
    db.session.add(bank)
    db.session.add(account)
    db.session.commit()

    may_transaction = Transaction(date='2020-05-15', description='Mexican place', amount=1500, account=account)
    june_transaction = Transaction(date='2020-06-21', description='Italian restaurant', amount=2700, account=account)
    july_not_found_transaction = Transaction(date='2020-07-04', description='BBQ', amount=4000, account=account)
    july_found_transaction = Transaction(date='2020-07-21', description='Pizza Delivery', amount=2000, account=account)

    db.session.add(may_transaction)
    db.session.add(june_transaction)
    db.session.add(july_not_found_transaction)
    db.session.add(july_found_transaction)
    db.session.commit()

    response = client.get('/transactions?start_date=2020-07-01&end_date=2020-07-31&search_term=pizza+del', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()

    expected_month = 'July'
    expected_transactions = [ { 'id': 4, 'date': '2020-07-21', 'description': 'Pizza Delivery', 'amount': '20.00' } ]

    response_month = json_response[0]
    assert response_month['month'] == expected_month
    assert response_month['transactions'] == expected_transactions


def test_transactions_search_term_found_two_transactions(client, login_test_user):
    access_token = login_test_user

    user = User.query.filter_by(email='john@test.com').first()

    bank = Bank(
            name='Ally Bank',
            access_token='fake access token',
            logo='fake logo',
            user=user
            )
    account = Account(
            plaid_account_id='fake account id',
            name='Checking Account',
            type='checking',
            bank=bank
            )
    db.session.add(bank)
    db.session.add(account)
    db.session.commit()

    may_transaction = Transaction(date='2020-05-15', description='Mexican place', amount=1500, account=account)
    june_transaction = Transaction(date='2020-06-21', description='Italian restaurant', amount=2700, account=account)
    july_found_transaction_one = Transaction(date='2020-07-01', description='Pizza Delivery', amount=1500, account=account)
    july_not_found_transaction = Transaction(date='2020-07-04', description='BBQ', amount=4000, account=account)
    july_found_transaction_two = Transaction(date='2020-07-21', description='Pizza Delivery', amount=2000, account=account)

    db.session.add(may_transaction)
    db.session.add(june_transaction)
    db.session.add(july_found_transaction_one)
    db.session.add(july_not_found_transaction)
    db.session.add(july_found_transaction_two)
    db.session.commit()

    access_token = login_test_user

    response = client.get('/transactions?start_date=2020-07-01&end_date=2020-07-31&search_term=pizza+del', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()

    expected_month = 'July'
    expected_transactions = [
            { 'id': 5, 'date': '2020-07-21', 'description': 'Pizza Delivery', 'amount': '20.00' },
            { 'id': 3, 'date': '2020-07-01', 'description': 'Pizza Delivery', 'amount': '15.00' }
            ]

    response_month = json_response[0]
    assert response_month['month'] == expected_month
    assert response_month['transactions'] == expected_transactions


def test_transactions_search_term_not_found(client, login_test_user):
    access_token = login_test_user

    user = User.query.filter_by(email='john@test.com').first()

    bank = Bank(
            name='Ally Bank',
            access_token='fake access token',
            logo='fake logo',
            user=user
            )
    account = Account(
            plaid_account_id='fake account id',
            name='Checking Account',
            type='checking',
            bank=bank
            )
    db.session.add(bank)
    db.session.add(account)
    db.session.commit()

    may_transaction = Transaction(date='2020-05-15', description='Mexican place', amount=1500, account=account)
    june_transaction = Transaction(date='2020-06-21', description='Italian restaurant', amount=2700, account=account)
    july_transaction = Transaction(date='2020-07-04', description='BBQ', amount=4000, account=account)

    db.session.add(may_transaction)
    db.session.add(june_transaction)
    db.session.add(july_transaction)
    db.session.commit()

    access_token = login_test_user

    response = client.get('/transactions?start_date=2020-06-01&end_date=2020-06-30&search_term=japanese', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()

    assert json_response == []

def test_transactions_add(client, login_test_user):
    no_transaction = Transaction.query.filter_by(date='2020-10-04', description='Coffee').first()
    assert no_transaction is None

    access_token = login_test_user

    user = User.query.filter_by(email='john@test.com').first()

    bank = Bank(
            name='Ally Bank',
            access_token='fake access token',
            logo='fake logo',
            user=user
            )
    account = Account(
            plaid_account_id='fake account id',
            name='Checking Account',
            type='checking',
            bank=bank
            )
    db.session.add(bank)
    db.session.add(account)
    db.session.commit()

    request_body = {
            'date': '2020-10-04',
            'description': 'Coffee',
            'amount': '14.00'
    }

    response = client.post('/transactions/create', headers={ "Authorization": f"Bearer {access_token}" }, json=request_body)
    response_body = response.get_json()

    assert response_body['message'] == 'Transaction successfully created'

    added_transaction = Transaction.query.filter_by(date='2020-10-04', description='Coffee').first()
    assert added_transaction.date == date(2020, 10, 4)
    assert added_transaction.description == 'Coffee'
    assert added_transaction.amount == 1400

def test_transactions_add_duplicate(client, login_test_user):
    access_token = login_test_user

    user = User.query.filter_by(email='john@test.com').first()

    bank = Bank(
            name='Ally Bank',
            access_token='fake access token',
            logo='fake logo',
            user=user
            )
    account = Account(
            plaid_account_id='fake account id',
            name='Checking Account',
            type='checking',
            bank=bank
            )
    db.session.add(bank)
    db.session.add(account)
    db.session.commit()

    transaction = Transaction(
            date='2020-10-04',
            description='Coffee',
            amount=1400,
            account=account
            )
    db.session.add(transaction)
    db.session.commit()

    request_body = {
            'date': '2020-10-04',
            'description': 'Coffee',
            'amount': '14.00'
    }

    response = client.post('/transactions/create', headers={ "Authorization": f"Bearer {access_token}" }, json=request_body)
    response_body = response.get_json()

    assert response.status_code == 501
    assert response_body['message'] == 'Cannot create this transaction because it already exists'

def test_unauthorized_transactions_add(client):
    request_body = {
            'date': '2020-10-04',
            'description': 'Coffee',
            'amount': '14.00'
    }

    response = client.post('/transactions/create', json=request_body)
    json_response = response.get_json()
    assert json_response['msg'] == 'Missing Authorization Header'


def test_invalid_format_transaction_add(client, login_test_user):
    access_token = login_test_user

    request_body = {
            'date': '2020-10-04',
            'description': 'Coffee',
            'amount': '14.00'
    }

    response = client.post('/transactions/create', headers={ "Authorization": f"Bearer {access_token}" }, data=request_body)
    response_body = response.get_json()
    message = response_body['message']

    assert message == "Invalid format: body must be JSON"
    assert response.status_code == 501

def test_invalid_body_transaction_add(client, login_test_user):
    access_token = login_test_user

    for attribute in ['date', 'description', 'amount']:
        invalid_body = {
            'date': '2020-10-04',
            'description': 'Coffee',
            'amount': '14.00'
            }
        invalid_body.pop(attribute)
        response = client.post('/transactions/create', headers={ "Authorization": f"Bearer {access_token}" }, json=invalid_body)
        response_body = response.get_json()
        message = response_body['message']

        assert message == "Invalid format: body must contain date, description and amount"
        assert response.status_code == 501

def test_valid_transaction_delete(client, login_test_user):
    access_token = login_test_user

    user = User.query.filter_by(email='john@test.com').first()

    discretionary_spending = SpendingPlanPart(
            category = 'Discretionary Spending',
            label = 'Spending Money',
            search_term = '*',
            expected_amount = 0,
            user=user
            )
    db.session.add(discretionary_spending)
    db.session.commit()

    bank = Bank(
            name='Ally Bank',
            access_token='fake access token',
            logo='fake logo',
            user=user
            )
    account = Account(
            plaid_account_id='fake account id',
            name='Checking Account',
            type='checking',
            bank=bank
            )
    db.session.add(bank)
    db.session.add(account)
    db.session.commit()

    transaction = Transaction(
            date='2020-10-04',
            description='Coffee',
            amount=1400,
            account=account,
            spending_plan_part=discretionary_spending
            )
    db.session.add(transaction)
    db.session.commit()

    response = client.delete('/transactions/1', headers={ "Authorization": f"Bearer {access_token}" })
    response_body = response.get_json()

    message = response_body['message']

    assert message == "Transaction successfully deleted"
    assert response.status_code == 200

    deleted_transaction = Transaction.query.filter_by(date='2020-10-04', description='Coffee').first()
    assert deleted_transaction == None

def test_invalid_transaction_delete(client, login_test_user):
    access_token = login_test_user

    response = client.delete('/transactions/1', headers={ "Authorization": f"Bearer {access_token}" })
    response_body = response.get_json()

    message = response_body['message']

    assert message == "Cannot delete this transaction because it does not exist"
    assert response.status_code == 501

def test_valid_transaction_update(client, login_test_user):
    access_token = login_test_user

    user = User.query.filter_by(email='john@test.com').first()

    bank = Bank(
            name='Ally Bank',
            access_token='fake access token',
            logo='fake logo',
            user=user
            )
    account = Account(
            plaid_account_id='fake account id',
            name='Checking Account',
            type='checking',
            bank=bank
            )
    db.session.add(bank)
    db.session.add(account)
    db.session.commit()

    transaction = Transaction(
            date='2020-10-04',
            description='Coffee',
            amount=1400,
            account=account
            )
    db.session.add(transaction)
    db.session.commit()

    request_body = {
            'date': '2020-10-04',
            'description': 'Coffee',
            'amount': '4.00'
    }

    response = client.put('/transactions/1', headers={ "Authorization": f"Bearer {access_token}" }, json=request_body)
    response_body = response.get_json()

    assert response_body['message'] == 'Transaction successfully updated'

    updated_transaction = Transaction.query.get(1)
    assert updated_transaction.date == date(2020, 10, 4)
    assert updated_transaction.description == 'Coffee'
    assert updated_transaction.amount == 400

def test_invalid_body_transaction_update(client, login_test_user):
    access_token = login_test_user

    user = User.query.filter_by(email='john@test.com').first()

    bank = Bank(
            name='Ally Bank',
            access_token='fake access token',
            logo='fake logo',
            user=user
            )
    account = Account(
            plaid_account_id='fake account id',
            name='Checking Account',
            type='checking',
            bank=bank
            )
    db.session.add(bank)
    db.session.add(account)
    db.session.commit()

    transaction = Transaction(
            date='2020-10-04',
            description='Coffee',
            amount=1400,
            account=account
            )
    db.session.add(transaction)
    db.session.commit()

    for attribute in ['date', 'description', 'amount']:
        invalid_body = {
            'date': '2020-10-04',
            'description': 'Coffee',
            'amount': '14.00'
            }
        invalid_body.pop(attribute)
        response = client.put('/transactions/1', headers={ "Authorization": f"Bearer {access_token}" }, json=invalid_body)
        response_body = response.get_json()
        message = response_body['message']

        assert message == "Invalid format: body must contain date, description and amount"
        assert response.status_code == 501

def test_invalid_transaction_update(client, login_test_user):
    access_token = login_test_user

    request_body = {
            'date': '2020-10-04',
            'description': 'Coffee',
            'amount': '4.00'
    }

    response = client.put('/transactions/1', headers={ "Authorization": f"Bearer {access_token}" }, json=request_body)
    response_body = response.get_json()

    message = response_body['message']

    assert message == "Cannot update this transaction because it does not exist"
    assert response.status_code == 501

def test_invalid_format_transaction_update(client, login_test_user):
    access_token = login_test_user

    user = User.query.filter_by(email='john@test.com').first()

    bank = Bank(
            name='Ally Bank',
            access_token='fake access token',
            logo='fake logo',
            user=user
            )
    account = Account(
            plaid_account_id='fake account id',
            name='Checking Account',
            type='checking',
            bank=bank
            )
    db.session.add(bank)
    db.session.add(account)
    db.session.commit()

    transaction = Transaction(
            date='2020-10-04',
            description='Coffee',
            amount=1400,
            account=account
            )
    db.session.add(transaction)
    db.session.commit()

    request_body = {
        'date': '2020-10-04',
        'description': 'Coffee',
        'amount': '4.00'
    }

    response = client.put('/transactions/1', headers={ "Authorization": f"Bearer {access_token}" }, data=request_body)
    response_body = response.get_json()
    message = response_body['message']

    assert message == "Invalid format: body must be JSON"
    assert response.status_code == 501


