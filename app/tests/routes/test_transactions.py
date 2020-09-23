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
    assert json_response["message"] == 'Query parameters not found. Please provide dates or a search term in the request'

def test_transactions_date_range(client):
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

    login_response = client.post('/auth/login', json={
        'email': 'jessica@test.com',
        'password': 'password'
        })
    json_login_response = login_response.get_json()
    access_token = json_login_response['access_token']

    response = client.get('/transactions?start_date=2020-06-01&end_date=2020-06-30', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()

    assert [{ 'date': '2020-06-21', 'description': 'Italian restaurant', 'amount': 2700} ] == json_response['transactions']