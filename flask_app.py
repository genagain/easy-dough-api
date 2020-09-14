import os
from datetime import datetime, timedelta
import random
import string

from flask_bcrypt import generate_password_hash
from plaid import Client

from app import create_app, db, scheduler
from app.models import User, Transaction


app = create_app()

def add_user():
    print('Tick! The time is: %s' % datetime.now())
    with app.app_context():
        hashed_password = generate_password_hash('test_password').decode('utf-8')
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(5))
        user = User(
                firstname='Random',
                lastname='Test',
                email=f"{result_str}@test.com",
                password=hashed_password
                )
        db.session.add(user)
        db.session.commit()

def print_transactions():
    print('Tick! The time is: %s' % datetime.now())
    PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
    PLAID_SECRET = os.getenv('PLAID_SECRET')
    PLAID_ENV = os.getenv('PLAID_ENV', 'sandbox')
    ## TODO make sure access tokens persisted at the user/account level
    access_token = os.getenv('ACCESS_TOKEN')
    client = Client(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET, environment=PLAID_ENV, api_version='2019-05-29')
    # TODO change this to a day's worth of transactions once I have live data
    start_date = '{:%Y-%m-%d}'.format(datetime.now() + timedelta(-30))
    end_date = '{:%Y-%m-%d}'.format(datetime.now())
    transactions_response = client.Transactions.get(access_token, start_date, end_date)
    transactions_data = transactions_response['transactions']
    with app.app_context():
        # TODO use a try catch block if there is a uniqueness constraint on this column
        for transaction_datum in transactions_data:
            date = transaction_datum['date']
            description = transaction_datum['name']
            amount = int(transaction_datum['amount']) * 100
            transaction = Transaction(
                           date=date,
                           description=description,
                           amount=amount
                           )
            db.session.add(transaction)
            db.session.commit()



scheduler.add_job(add_user, 'cron', hour=1)
scheduler.add_job(print_transactions, 'cron', hour=2)
scheduler.start()
