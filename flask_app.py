import os
from datetime import datetime, timedelta
import random
import string

from flask_bcrypt import generate_password_hash
from plaid import Client

from app import create_app, db, scheduler
from app.models.user import User


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
    access_token = os.getenv('ACCESS_TOKEN')
    client = Client(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET, environment=PLAID_ENV, api_version='2019-05-29')
    start_date = '{:%Y-%m-%d}'.format(datetime.now() + timedelta(-30))
    end_date = '{:%Y-%m-%d}'.format(datetime.now())
    transactions_response = client.Transactions.get(access_token, start_date, end_date)
    print(transactions_response['accounts'])

# scheduler.add_job(add_user, 'cron', hour=1, minute=15)
scheduler.add_job(print_transactions, 'interval', minutes=2)
scheduler.start()
