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


def test_transactions_valid_date_range(client):
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

    assert [{ 'date': '2020-06-21', 'description': 'Italian restaurant', 'amount': 27.00} ] == json_response['transactions']

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


def test_transactions_search_term_found(client):
    hashed_password = generate_password_hash('password').decode('utf-8')
    user = User(
            firstname='Joseph',
            lastname='Test',
            email='joseph@test.com',
            password=hashed_password
            )
    db.session.add(user)
    db.session.commit()

    may_transaction = Transaction(date='2020-05-15', description='Mexican place', amount=1500)
    june_not_found_transaction = Transaction(date='2020-06-21', description='Italian restaurant', amount=2700)
    june_found_transaction = Transaction(date='2020-06-21', description='Pizza Delivery', amount=2000)
    july_transaction = Transaction(date='2020-07-04', description='BBQ', amount=4000)

    db.session.add(may_transaction)
    db.session.add(june_not_found_transaction)
    db.session.add(june_found_transaction)
    db.session.add(july_transaction)
    db.session.commit()

    login_response = client.post('/auth/login', json={
        'email': 'joseph@test.com',
        'password': 'password'
        })
    json_login_response = login_response.get_json()
    access_token = json_login_response['access_token']

    response = client.get('/transactions?start_date=2020-06-01&end_date=2020-06-30&search_term=pizza+del', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()

    assert [{ 'date': '2020-06-21', 'description': 'Pizza Delivery', 'amount': 20.00} ] == json_response['transactions']

def test_transactions_search_term_not_found(client):
    hashed_password = generate_password_hash('password').decode('utf-8')
    user = User(
            firstname='Jerome',
            lastname='Test',
            email='jerome@test.com',
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
        'email': 'jerome@test.com',
        'password': 'password'
        })
    json_login_response = login_response.get_json()
    access_token = json_login_response['access_token']

    response = client.get('/transactions?start_date=2020-06-01&end_date=2020-06-30&search_term=japanese', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()

    assert 'No transactions were found that matched the provided search term or date range'== json_response['message']

