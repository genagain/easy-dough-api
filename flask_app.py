import os
from datetime import datetime, timedelta
import random
import string

from sqlalchemy.exc import IntegrityError
from plaid import Client

from app import create_app, db, scheduler, plaid_client
from app.models import User, Bank, Transaction, SpendingPlanPart


app = create_app()

def print_transactions():
    print('Tick! The time is: %s' % datetime.now())
    yesterday = '{:%Y-%m-%d}'.format(datetime.now() + timedelta(-1))
    with app.app_context():
        banks = Bank.query.all()
        for bank in banks:
            accounts_by_id = dict(list(map(lambda account: [account.plaid_account_id, account], bank.accounts)))
            access_token = bank.access_token
            transactions_response = plaid_client.Transactions.get(access_token, yesterday, yesterday)
            transactions_data = transactions_response['transactions']
            user = bank.user
            discretionary_spending = SpendingPlanPart.query.filter_by(category="Discretionary Spending", user=user).first()
            for transaction_datum in transactions_data:
                # TODO create a transactions class method
                try:
                    date = transaction_datum['date']
                    description = transaction_datum['name']
                    amount = int(transaction_datum['amount']) * 100
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

        users = User.query.all()
        for user in users:
            user.categorize_transactions(yesterday, yesterday)

scheduler.add_job(print_transactions, 'cron', hour=2)
scheduler.start()
