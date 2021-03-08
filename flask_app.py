import os
from datetime import datetime, timedelta
import logging
import random
import string

from sqlalchemy.exc import IntegrityError
from plaid import Client

from app import create_app, db, scheduler, plaid_client
from app.models import User, Bank, Transaction, SpendingPlanPart


app = create_app()

def ingest_transactions():
    print('Tick! The time is: %s' % datetime.now())
    start_date = '{:%Y-%m-%d}'.format(datetime.now() + timedelta(-8))
    end_date = '{:%Y-%m-%d}'.format(datetime.now() + timedelta(-1))
    with app.app_context():
        users = User.query.filter(User.email.notlike('john@test.com')).all()
        for user in users:
            print(user.email)
            banks = user.banks
            discretionary_spending = SpendingPlanPart.query.filter_by(category="Discretionary Spending", user=user).first()

            for bank in banks:
                accounts_by_id = dict(list(map(lambda account: [account.plaid_account_id, account], bank.accounts)))
                access_token = bank.access_token
                transactions_data = []
                try:
                    transactions_response = plaid_client.Transactions.get(access_token, start_date, end_date)
                    transactions_data = transactions_response['transactions']
                except Exception as e:
                    print(e)
                    logging.error('Error at %s', 'Plaid', exc_info=e)
                    continue

                for transaction_datum in transactions_data:
                    if transaction_datum['pending']:
                        continue
                    else:
                        try:
                            date = transaction_datum['date']
                            description = transaction_datum['name']
                            amount = float(transaction_datum['amount']) * 100
                            account = accounts_by_id[transaction_datum['account_id']]
                            transaction = Transaction(
                                           date=date,
                                           description=description,
                                           amount=amount,
                                           account=account,
                                           spending_plan_part=discretionary_spending
                                           )
                            db.session.add(transaction)
                            db.session.commit()
                        except IntegrityError:
                            db.session.rollback()
            user.categorize_transactions(start_date, end_date)

ingest_transactions()
scheduler.add_job(ingest_transactions, 'cron', hour=23, timezone='America/Los_Angeles')
scheduler.start()
