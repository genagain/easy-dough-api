from datetime import date
import pytest

from flask_bcrypt import generate_password_hash
from app import db
from app.models import User, Transaction
from .utils import client

def test_unauthorized_transactions(client):
    response = client.get('/transactions')
    json_response = response.get_json()
    assert json_response['msg'] == 'Missing Authorization Header'

def test_transactions_no_query_params(client):
    hashed_password = generate_password_hash('password').decode('utf-8')
    user = User(
            firstname='Jessica',
            lastname='Test',
            email='jessica@test.com',
            password=hashed_password
            )
    db.session.add(user)
    db.session.commit()

    login_response = client.post('/auth/login', json={
        'email': 'jessica@test.com',
        'password': 'password'
        })
    json_login_response = login_response.get_json()
    access_token = json_login_response['access_token']

    response = client.get('/transactions', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()
    assert json_response["message"] == 'Query parameters not found. Please provide both a start date and end date and optionally a search term in the request'


def test_transactions_invalid_query_params(client):
    hashed_password = generate_password_hash('password').decode('utf-8')
    user = User(
            firstname='Javier',
            lastname='Test',
            email='javier@test.com',
            password=hashed_password
            )
    db.session.add(user)
    db.session.commit()

    login_response = client.post('/auth/login', json={
        'email': 'javier@test.com',
        'password': 'password'
        })
    json_login_response = login_response.get_json()
    access_token = json_login_response['access_token']

    response = client.get('/transactions?something=invalid', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()
    assert json_response["message"] == 'Query parameters not found. Please provide both a start date and end date and optionally a search term in the request'


def test_transactions_one_month_one_transaction(client):
    ## TODO create add user class method
    hashed_password = generate_password_hash('password').decode('utf-8')
    user = User(
            firstname='Justin',
            lastname='Test',
            email='justin@test.com',
            password=hashed_password
            )
    db.session.add(user)
    db.session.commit()

    may_transaction = Transaction(date='2020-05-15', description='Mexican place', amount=1500)
    june_transaction = Transaction(date='2020-06-21', description='Italian restaurant', amount=2700)
    july_transaction = Transaction(date='2020-07-04', description='BBQ', amount=4000)

    db.session.add(may_transaction)
    db.session.add(june_transaction)
    db.session.add(july_transaction)
    db.session.commit()

    # TODO create login helper function
    login_response = client.post('/auth/login', json={
        'email': 'justin@test.com',
        'password': 'password'
        })
    json_login_response = login_response.get_json()
    access_token = json_login_response['access_token']

    response = client.get('/transactions?start_date=2020-06-01&end_date=2020-06-30', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()

    expected_month = 'June'
    expected_transactions = [ { 'date': '2020-06-21', 'description': 'Italian restaurant', 'amount': 27.00 } ]

    response_month = json_response[0]
    assert response_month['month'] == expected_month
    assert response_month['transactions'] == expected_transactions


def test_transactions_one_month_two_transactions(client):
    ## TODO create add user class method
    hashed_password = generate_password_hash('password').decode('utf-8')
    user = User(
            firstname='Justin',
            lastname='Test',
            email='justin@test.com',
            password=hashed_password
            )
    db.session.add(user)
    db.session.commit()

    may_transaction = Transaction(date='2020-05-15', description='Mexican place', amount=1500)
    june_transaction_one = Transaction(date='2020-06-09', description='Japanese restaurant', amount=2300)
    june_transaction_two = Transaction(date='2020-06-21', description='Italian restaurant', amount=2700)
    july_transaction = Transaction(date='2020-07-04', description='BBQ', amount=4000)

    db.session.add(may_transaction)
    db.session.add(june_transaction_one)
    db.session.add(june_transaction_two)
    db.session.add(july_transaction)
    db.session.commit()

    # TODO create login helper function
    login_response = client.post('/auth/login', json={
        'email': 'justin@test.com',
        'password': 'password'
        })
    json_login_response = login_response.get_json()
    access_token = json_login_response['access_token']

    response = client.get('/transactions?start_date=2020-06-01&end_date=2020-06-30', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()

    expected_month = 'June'
    expected_transactions = [
            { 'date': '2020-06-21', 'description': 'Italian restaurant', 'amount': 27.00 },
            { 'date': '2020-06-09', 'description': 'Japanese restaurant', 'amount': 23.00 }
            ]

    response_month = json_response[0]
    assert response_month['month'] == expected_month
    assert response_month['transactions'] == expected_transactions

def test_transactions_one_month_not_found(client):
    ## TODO create add user class method
    hashed_password = generate_password_hash('password').decode('utf-8')
    user = User(
            firstname='Justin',
            lastname='Test',
            email='justin@test.com',
            password=hashed_password
            )
    db.session.add(user)
    db.session.commit()

    may_transaction = Transaction(date='2020-05-15', description='Mexican place', amount=1500)
    june_transaction_one = Transaction(date='2020-06-09', description='Japanese restaurant', amount=2300)
    june_transaction_two = Transaction(date='2020-06-21', description='Italian restaurant', amount=2700)
    july_transaction = Transaction(date='2020-07-04', description='BBQ', amount=4000)

    db.session.add(may_transaction)
    db.session.add(june_transaction_one)
    db.session.add(june_transaction_two)
    db.session.add(july_transaction)
    db.session.commit()

    # TODO create login helper function
    login_response = client.post('/auth/login', json={
        'email': 'justin@test.com',
        'password': 'password'
        })
    json_login_response = login_response.get_json()
    access_token = json_login_response['access_token']

    response = client.get('/transactions?start_date=2020-01-01&end_date=2020-01-31', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()

    assert json_response == []


def test_transactions_no_start_date(client):
    hashed_password = generate_password_hash('password').decode('utf-8')
    user = User(
            firstname='Jonah',
            lastname='Test',
            email='jonah@test.com',
            password=hashed_password
            )
    db.session.add(user)
    db.session.commit()

    may_transaction = Transaction(date='2020-05-15', description='Mexican place', amount=1500)
    june_transaction = Transaction(date='2020-06-21', description='Italian restaurant', amount=2700)
    july_transaction = Transaction(date='2020-07-04', description='BBQ', amount=4000)

    db.session.add(may_transaction)
    db.session.add(june_transaction)
    db.session.add(july_transaction)
    db.session.commit()

    login_response = client.post('/auth/login', json={
        'email': 'jonah@test.com',
        'password': 'password'
        })
    json_login_response = login_response.get_json()
    access_token = json_login_response['access_token']

    response = client.get('/transactions?end_date=2020-06-30', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()

    assert 'start_date and end_date query parameters not found. Please provide both a start date and end date' == json_response['message']


def test_transactions_no_end_date(client):
    hashed_password = generate_password_hash('password').decode('utf-8')
    user = User(
            firstname='Joy',
            lastname='Test',
            email='joy@test.com',
            password=hashed_password
            )
    db.session.add(user)
    db.session.commit()

    may_transaction = Transaction(date='2020-05-15', description='Mexican place', amount=1500)
    june_transaction = Transaction(date='2020-06-21', description='Italian restaurant', amount=2700)
    july_transaction = Transaction(date='2020-07-04', description='BBQ', amount=4000)

    db.session.add(may_transaction)
    db.session.add(june_transaction)
    db.session.add(july_transaction)
    db.session.commit()

    login_response = client.post('/auth/login', json={
        'email': 'joy@test.com',
        'password': 'password'
        })
    json_login_response = login_response.get_json()
    access_token = json_login_response['access_token']

    response = client.get('/transactions?start_date=2020-06-30', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()

    assert 'start_date and end_date query parameters not found. Please provide both a start date and end date' == json_response['message']


def test_transactions_search_term_found_one_transaction(client):
    hashed_password = generate_password_hash('password').decode('utf-8')
    user = User(
            firstname='John',
            lastname='Doe',
            email='john@test.com',
            password=hashed_password
            )
    db.session.add(user)
    db.session.commit()

    may_transaction = Transaction(date='2020-05-15', description='Mexican place', amount=1500)
    june_transaction = Transaction(date='2020-06-21', description='Italian restaurant', amount=2700)
    july_not_found_transaction = Transaction(date='2020-07-04', description='BBQ', amount=4000)
    july_found_transaction = Transaction(date='2020-07-21', description='Pizza Delivery', amount=2000)

    db.session.add(may_transaction)
    db.session.add(june_transaction)
    db.session.add(july_not_found_transaction)
    db.session.add(july_found_transaction)
    db.session.commit()

    login_response = client.post('/auth/login', json={
        'email': 'john@test.com',
        'password': 'password'
        })
    json_login_response = login_response.get_json()
    access_token = json_login_response['access_token']

    response = client.get('/transactions?start_date=2020-07-01&end_date=2020-07-31&search_term=pizza+del', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()

    expected_month = 'July'
    expected_transactions = [ { 'date': '2020-07-21', 'description': 'Pizza Delivery', 'amount': 20.00 } ]

    response_month = json_response[0]
    assert response_month['month'] == expected_month
    assert response_month['transactions'] == expected_transactions


def test_transactions_search_term_found_two_transactions(client):
    hashed_password = generate_password_hash('password').decode('utf-8')
    user = User(
            firstname='John',
            lastname='Doe',
            email='john@test.com',
            password=hashed_password
            )
    db.session.add(user)
    db.session.commit()

    may_transaction = Transaction(date='2020-05-15', description='Mexican place', amount=1500)
    june_transaction = Transaction(date='2020-06-21', description='Italian restaurant', amount=2700)
    july_found_transaction_one = Transaction(date='2020-07-01', description='Pizza Delivery', amount=1500)
    july_not_found_transaction = Transaction(date='2020-07-04', description='BBQ', amount=4000)
    july_found_transaction_two = Transaction(date='2020-07-21', description='Pizza Delivery', amount=2000)

    db.session.add(may_transaction)
    db.session.add(june_transaction)
    db.session.add(july_found_transaction_one)
    db.session.add(july_not_found_transaction)
    db.session.add(july_found_transaction_two)
    db.session.commit()

    login_response = client.post('/auth/login', json={
        'email': 'john@test.com',
        'password': 'password'
        })
    json_login_response = login_response.get_json()
    access_token = json_login_response['access_token']

    response = client.get('/transactions?start_date=2020-07-01&end_date=2020-07-31&search_term=pizza+del', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()

    expected_month = 'July'
    expected_transactions = [
            { 'date': '2020-07-21', 'description': 'Pizza Delivery', 'amount': 20.00 },
            { 'date': '2020-07-01', 'description': 'Pizza Delivery', 'amount': 15.00 }
            ]

    response_month = json_response[0]
    assert response_month['month'] == expected_month
    assert response_month['transactions'] == expected_transactions


def test_transactions_search_term_not_found(client):
    hashed_password = generate_password_hash('password').decode('utf-8')
    user = User(
            firstname='John',
            lastname='Doe',
            email='john@test.com',
            password=hashed_password
            )
    db.session.add(user)
    db.session.commit()

    may_transaction = Transaction(date='2020-05-15', description='Mexican place', amount=1500)
    june_transaction = Transaction(date='2020-06-21', description='Italian restaurant', amount=2700)
    july_transaction = Transaction(date='2020-07-04', description='BBQ', amount=4000)

    db.session.add(may_transaction)
    db.session.add(june_transaction)
    db.session.add(july_transaction)
    db.session.commit()

    login_response = client.post('/auth/login', json={
        'email': 'john@test.com',
        'password': 'password'
        })
    json_login_response = login_response.get_json()
    access_token = json_login_response['access_token']

    response = client.get('/transactions?start_date=2020-06-01&end_date=2020-06-30&search_term=japanese', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()

    assert json_response == []

def test_transactions_add(client):
    hashed_password = generate_password_hash('password').decode('utf-8')
    user = User(
            firstname='John',
            lastname='Doe',
            email='john@test.com',
            password=hashed_password
            )
    db.session.add(user)
    db.session.commit()

    no_transaction = Transaction.query.filter_by(date='2020-10-04', description='Coffee').first()
    assert no_transaction is None

    login_response = client.post('/auth/login', json={
        'email': 'john@test.com',
        'password': 'password'
        })
    json_login_response = login_response.get_json()
    access_token = json_login_response['access_token']

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

