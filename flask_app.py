import os
from datetime import datetime, timedelta
import random
import string

from flask_bcrypt import generate_password_hash
from plaid import Client

from app import create_app, db, scheduler, plaid_client
from app.models import User, Bank, Transaction


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
    with app.app_context():
        banks = Bank.query.all()
        for bank in banks:
            # TODO create accounts by id dict
            accounts = bank.accounts
            access_token = bank.access_token
            start_date = '2020-07-15'
            end_date = '2020-12-15'
            # TODO change this to a day's worth of transactions once I have live data
            # start_date = '{:%Y-%m-%d}'.format(datetime.now() + timedelta(-30))
            # end_date = '{:%Y-%m-%d}'.format(datetime.now())
            transactions_response = plaid_client.Transactions.get(access_token, start_date, end_date)
            transactions_data = transactions_response['transactions']
            for transaction_datum in transactions_data:
                # TODO create a transactions class method
                # TODO make sure the transactions are associated to the correct account using the plaid account id
                # TODO use a try catch block if there is a uniqueness constraint on this column
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
