import pytest

from app import db
from app.models import User, Bank, Account, Transaction, SpendingPlanPart
from .utils import client, login_test_user

def test_months(client, login_test_user):
    access_token = login_test_user

    user = User.query.filter_by(email='john@test.com').first()
    discretionary_spending = SpendingPlanPart(
            category = 'Discretionary Spending',
            label = 'Spending Money',
            search_term = '*',
            expected_amount = 0,
            user=user
            )

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

    may_transaction = Transaction(date='2020-05-15', description='Mexican place', amount=1500, account=account, spending_plan_part=discretionary_spending)
    june_transaction_one = Transaction(date='2020-06-21', description='Italian restaurant', amount=2700, account=account, spending_plan_part=discretionary_spending)
    june_transaction_two = Transaction(date='2020-06-24', description='Japanese restaurant', amount=3500, account=account, spending_plan_part=discretionary_spending)
    july_transaction = Transaction(date='2020-07-04', description='BBQ', amount=4000, account=account, spending_plan_part=discretionary_spending)

    db.session.add(may_transaction)
    db.session.add(june_transaction_one)
    db.session.add(june_transaction_two)
    db.session.add(july_transaction)
    db.session.commit()

    response = client.get('/reports/months', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()

    expected_months = [
            'May',
            'June',
            'July'
    ]

    assert json_response['months'] == expected_months

def test_generate_report(client, login_test_user):
    access_token = login_test_user

    user = User.query.filter_by(email='john@test.com').first()
    discretionary_spending = SpendingPlanPart(
            category = 'Discretionary Spending',
            label = 'Spending Money',
            search_term = '*',
            expected_amount = 10000,
            user=user
            )

    groceries = SpendingPlanPart(
            category = 'Fixed Costs',
            label = 'Groceries',
            search_term = 'Grocery Store',
            expected_amount = 20000,
            user=user
            )

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

    may_transaction = Transaction(date='2020-05-15', description='Mexican place', amount=1500, account=account, spending_plan_part=discretionary_spending)
    june_transaction_one = Transaction(date='2020-06-10', description='Grocery Store', amount=7000, account=account, spending_plan_part=groceries)
    june_transaction_two = Transaction(date='2020-06-15', description='Italian restaurant', amount=2950, account=account, spending_plan_part=discretionary_spending)
    june_transaction_three = Transaction(date='2020-06-21', description='Grocery Store', amount=6400, account=account, spending_plan_part=groceries)
    june_transaction_four = Transaction(date='2020-06-26', description='Japanese restaurant', amount=3500, account=account, spending_plan_part=discretionary_spending)
    july_transaction = Transaction(date='2020-07-04', description='BBQ', amount=4000, account=account, spending_plan_part=discretionary_spending)

    db.session.add(may_transaction)
    db.session.add(june_transaction_one)
    db.session.add(june_transaction_two)
    db.session.add(june_transaction_three)
    db.session.add(june_transaction_four)
    db.session.add(july_transaction)
    db.session.commit()

    response = client.get('/reports/generate?month=June', headers={ "Authorization": f"Bearer {access_token}" })
    json_response = response.get_json()

    expected_reponse = [
            {
                'label': "Groceries",
                'actualAmount': 134.0,
                'expectedAmount': 200,
                'difference': 66.0
            },
            {
                'label': "Spending Money",
                'actualAmount': 64.5,
                'expectedAmount': 100,
                'difference': 35.5
            }
    ]

    assert json_response['historticalSpending'] == expected_reponse
