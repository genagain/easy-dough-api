from datetime import date
import pytest
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import check_password_hash

from app import create_app, db
from app.models import User, Transaction, Bank, Account, SpendingPlanPart

@pytest.fixture
def context():
    app = create_app()
    with app.app_context() as context:
        db.session.remove()
        db.drop_all()
        db.create_all()
        yield context

def test_create_user(context):
    user = User(
            firstname='John',
            lastname='Test',
            email='john@test.com',
            password='password'
            )
    db.session.add(user)
    db.session.commit()
    assert user.firstname == 'John'
    assert user.lastname == 'Test'
    assert user.email == 'john@test.com'
    assert user.password == 'password'

def test_unique_email_constraint_user(context):
    user = User(
            firstname='John',
            lastname='User',
            email='john@test.com',
            password='password'
            )
    db.session.add(user)
    db.session.commit()

    user1 = User(
            firstname='John',
            lastname='Test',
            email='john@test.com',
            password='test'
            )
    db.session.add(user1)
    with pytest.raises(IntegrityError) as error:
      db.session.commit()

def test_create_user_hashed_password(context):
    no_user = User.query.filter_by(email='john@test.com').first()
    assert no_user is None

    user = User.create(
                firstname='John',
                lastname='Doe',
                email='john@test.com',
                password='password'
            )

    assert user.firstname == 'John'
    assert user.lastname == 'Doe'
    assert user.email == 'john@test.com'
    assert check_password_hash(user.password, 'password')

def test_user_categorize_transactions(context):
    user = User(
            firstname='John',
            lastname='Test',
            email='john@test.com',
            password='password'
            )
    db.session.add(user)
    db.session.commit()

    discretionary_spending = SpendingPlanPart(
            category = 'Discretionary Spending',
            label = 'Spending Money',
            search_term = '*',
            expected_amount = 0,
            user=user
            )
    db.session.add(discretionary_spending)
    db.session.commit()

    rent = SpendingPlanPart(
            category='Fixed Costs',
            label='Rent',
            search_term='Property Management',
            expected_amount= 1000,
            user=user
            )
    db.session.add(rent)
    db.session.commit()

    emergency_fund = SpendingPlanPart(
            category='Savings',
            label='Emergency Fund',
            search_term='Employer',
            expected_amount= 800,
            user=user
            )
    db.session.add(emergency_fund)
    db.session.commit()

    stocks = SpendingPlanPart(
            category='Investments',
            label='Stocks',
            search_term='Brokerage',
            expected_amount= 600,
            user=user
            )
    db.session.add(stocks)
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

    transaction_1 = Transaction(
            date='2020-09-01',
            description='Lyft',
            amount='700',
            account=account,
            spending_plan_part=discretionary_spending
            )
    transaction_2 = Transaction(
            date='2020-09-01',
            description='PROPERTY MANAGEMENT',
            amount='1000',
            account=account,
            spending_plan_part=discretionary_spending
            )
    transaction_3 = Transaction(
            date='2020-09-01',
            description='EMPLOYER',
            amount='800',
            account=account,
            spending_plan_part=discretionary_spending
            )
    transaction_4 = Transaction(
            date='2020-09-01',
            description='BROKERAGE',
            amount='800',
            account=account,
            spending_plan_part=discretionary_spending
            )
    db.session.add(transaction_1)
    db.session.add(transaction_2)
    db.session.add(transaction_3)
    db.session.add(transaction_4)
    db.session.commit()

    user.categorize_transactions('2020-09-01', '2020-09-02')

    updated_transaction_1 = Transaction.query.filter_by(date='2020-09-01', description='Lyft').first()
    updated_transaction_2 = Transaction.query.filter_by(date='2020-09-01', description='PROPERTY MANAGEMENT').first()
    updated_transaction_3 = Transaction.query.filter_by(date='2020-09-01', description='EMPLOYER').first()
    updated_transaction_4 = Transaction.query.filter_by(date='2020-09-01', description='BROKERAGE').first()

    assert updated_transaction_1.spending_plan_part == discretionary_spending
    assert updated_transaction_2.spending_plan_part == rent
    assert updated_transaction_3.spending_plan_part == emergency_fund
    assert updated_transaction_4.spending_plan_part == stocks

def test_create_transaction(context):
    user = User(
            firstname='John',
            lastname='Test',
            email='john@test.com',
            password='password'
            )
    db.session.add(user)
    db.session.commit()

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
            date='2020-09-14',
            description='Lyft',
            amount='700',
            account=account,
            spending_plan_part=discretionary_spending
            )
    db.session.add(transaction)
    db.session.commit()
    assert transaction.date == date(2020, 9, 14)
    assert transaction.description == 'Lyft'
    assert transaction.amount == 700
    assert transaction.to_dict() == { 'id': 1, 'date': '2020-09-14', 'description': 'Lyft', 'amount': '7.00' }

def test_create_transaction_with_eleven_cents(context):
    user = User(
            firstname='John',
            lastname='Test',
            email='john@test.com',
            password='password'
            )
    db.session.add(user)
    db.session.commit()

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
            date='2020-09-14',
            description='Lyft',
            amount='711',
            account=account,
            spending_plan_part=discretionary_spending
            )
    db.session.add(transaction)
    db.session.commit()
    assert transaction.date == date(2020, 9, 14)
    assert transaction.description == 'Lyft'
    assert transaction.amount == 711
    assert transaction.to_dict() == { 'id': 1, 'date': '2020-09-14', 'description': 'Lyft', 'amount': '7.11' }

def test_unique_transaction(context):
    user = User(
            firstname='John',
            lastname='Test',
            email='john@test.com',
            password='password'
            )
    db.session.add(user)
    db.session.commit()

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
            date='2020-09-14',
            description='Lyft',
            amount='700',
            account=account,
            spending_plan_part=discretionary_spending
            )
    db.session.add(transaction)
    db.session.commit()

    transaction1 = Transaction(
            date='2020-09-14',
            description='Lyft',
            amount='700',
            account=account,
            spending_plan_part=discretionary_spending
            )
    db.session.add(transaction1)
    with pytest.raises(IntegrityError) as error:
      db.session.commit()

def test_valid_two_transactions(context):
    user = User(
            firstname='John',
            lastname='Test',
            email='john@test.com',
            password='password'
            )
    db.session.add(user)
    db.session.commit()

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

    other_user = User(
            firstname='Jane',
            lastname='Test',
            email='jane@test.com',
            password='password'
            )
    db.session.add(other_user)
    db.session.commit()

    other_bank = Bank(
            name='Ally Bank',
            access_token='other fake access token',
            logo='fake logo',
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

    transaction = Transaction(
            date='2020-09-14',
            description='Lyft',
            amount='700',
            account=account,
            spending_plan_part=discretionary_spending
            )
    db.session.add(transaction)
    db.session.commit()

    other_transaction = Transaction(
            date='2020-09-14',
            description='Lyft',
            amount='700',
            account=other_account,
            spending_plan_part=discretionary_spending
            )
    db.session.add(other_transaction)
    db.session.commit()

    assert transaction.date == date(2020, 9, 14)
    assert transaction.description == 'Lyft'
    assert transaction.amount == 700
    assert transaction.to_dict() == { 'id': 1, 'date': '2020-09-14', 'description': 'Lyft', 'amount': '7.00' }

    assert other_transaction.date == date(2020, 9, 14)
    assert other_transaction.description == 'Lyft'
    assert other_transaction.amount == 700
    assert other_transaction.to_dict() == { 'id': 2, 'date': '2020-09-14', 'description': 'Lyft', 'amount': '7.00' }

def test_valid_bank(context):
    user = User(
            firstname='John',
            lastname='Test',
            email='john@test.com',
            password='password'
            )
    db.session.add(user)
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

    assert bank.name == 'Ally Bank'
    assert bank.access_token == 'fake access token'
    assert bank.logo == 'fake logo'
    assert bank.user == user
    assert account in bank.accounts
    assert bank.accounts_to_dict() == [{ 'name': 'Checking Account', 'type': 'Checking'}]

def test_valid_two_banks(context):
    user = User(
            firstname='John',
            lastname='Test',
            email='john@test.com',
            password='password'
            )
    db.session.add(user)
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

    other_user = User(
            firstname='Jane',
            lastname='Test',
            email='jane@test.com',
            password='password'
            )
    db.session.add(other_user)
    db.session.commit()

    other_bank = Bank(
            name='Ally Bank',
            access_token='other fake access token',
            logo='fake logo',
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

    assert bank.name == 'Ally Bank'
    assert bank.access_token == 'fake access token'
    assert bank.logo == 'fake logo'
    assert bank.user == user
    assert account in bank.accounts
    assert bank.accounts_to_dict() == [{ 'name': 'Checking Account', 'type': 'Checking'}]

    assert other_bank.name == 'Ally Bank'
    assert other_bank.access_token == 'other fake access token'
    assert other_bank.logo == 'fake logo'
    assert other_bank.user == other_user
    assert other_account in other_bank.accounts
    assert other_bank.accounts_to_dict() == [{ 'name': 'Checking Account', 'type': 'Checking'}]

def test_unique_bank(context):
    user = User(
            firstname='John',
            lastname='Test',
            email='john@test.com',
            password='password'
            )
    db.session.add(user)
    db.session.commit()

    bank = Bank(
            name='Ally Bank',
            access_token='fake access token',
            logo='fake logo',
            user=user
            )
    db.session.add(bank)
    db.session.commit()

    bank1 = Bank(
            name='Ally Bank',
            access_token='another fake access token',
            logo='another fake logo',
            user=user
            )
    db.session.add(bank1)
    with pytest.raises(IntegrityError) as error:
      db.session.commit()

def test_valid_account(context):
    user = User(
            firstname='John',
            lastname='Test',
            email='john@test.com',
            password='password'
            )
    db.session.add(user)
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

    assert account.plaid_account_id == 'fake account id'
    assert account.name == 'Checking Account'
    assert account.type == 'checking'
    assert account.bank == bank
    assert account.to_dict() == { 'name': 'Checking Account', 'type': 'Checking' }

def test_unique_account(context):
    user = User(
            firstname='John',
            lastname='Test',
            email='john@test.com',
            password='password'
            )
    db.session.add(user)
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

    account1 = Account(
            plaid_account_id='fake account id',
            name='Checking Account',
            type='checking',
            bank=bank
            )
    db.session.add(account1)
    with pytest.raises(IntegrityError) as error:
      db.session.commit()


def test_valid_spending_plan_part(context):
    user = User(
            firstname='John',
            lastname='Test',
            email='john@test.com',
            password='password'
            )
    db.session.add(user)
    db.session.commit()

    spending_plan_part = SpendingPlanPart(
            category='Discretionary Spending',
            label='Spending Money',
            search_term='*',
            expected_amount=0,
            user=user
            )
    db.session.add(spending_plan_part)
    db.session.commit()

    assert spending_plan_part.category == 'Discretionary Spending'
    assert spending_plan_part.label == 'Spending Money'
    assert spending_plan_part.search_term == '*'
    assert spending_plan_part.expected_amount == 0
    assert spending_plan_part.user == user
    assert spending_plan_part.to_dict() == { 'id': 1, 'label': 'Spending Money', 'searchTerm': '*', 'expectedAmount': '0.00' }

def test_valid_spending_plan_part_with_eleven_cents(context):
    user = User(
            firstname='John',
            lastname='Test',
            email='john@test.com',
            password='password'
            )
    db.session.add(user)
    db.session.commit()

    spending_plan_part = SpendingPlanPart(
            category='Discretionary Spending',
            label='Spending Money',
            search_term='*',
            expected_amount=1011,
            user=user
            )
    db.session.add(spending_plan_part)
    db.session.commit()

    assert spending_plan_part.category == 'Discretionary Spending'
    assert spending_plan_part.label == 'Spending Money'
    assert spending_plan_part.search_term == '*'
    assert spending_plan_part.expected_amount == 1011
    assert spending_plan_part.user == user
    assert spending_plan_part.to_dict() == { 'id': 1, 'label': 'Spending Money', 'searchTerm': '*', 'expectedAmount': '10.11' }


def test_invalid_spending_plan_part(context):
    user = User(
            firstname='John',
            lastname='Test',
            email='john@test.com',
            password='password'
            )
    db.session.add(user)
    db.session.commit()

    with pytest.raises(ValueError) as error:
        spending_plan_part = SpendingPlanPart(
            category='invalid category',
            label='Spending Money',
            search_term='*',
            expected_amount=0,
            user=user
            )


def test_unique_spending_plan_part(context):
    user = User(
            firstname='John',
            lastname='Test',
            email='john@test.com',
            password='password'
            )
    db.session.add(user)
    db.session.commit()

    spending_plan_part = SpendingPlanPart(
            category='Discretionary Spending',
            label='Spending Money',
            search_term='*',
            expected_amount=0,
            user=user
            )
    db.session.add(spending_plan_part)
    db.session.commit()

    spending_plan_part1 = SpendingPlanPart(
            category='Discretionary Spending',
            label='Spending Money',
            search_term='*',
            expected_amount=0,
            user=user
            )
    db.session.add(spending_plan_part1)
    with pytest.raises(IntegrityError) as error:
        db.session.commit()
