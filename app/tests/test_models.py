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

def test_create_transaction(context):
    transaction = Transaction(
            date='2020-09-14',
            description='Lyft',
            amount='700'
            )
    db.session.add(transaction)
    db.session.commit()
    assert transaction.date == date(2020, 9, 14)
    assert transaction.description == 'Lyft'
    assert transaction.amount == 700
    assert transaction.to_dict() == { 'id': 1, 'date': '2020-09-14', 'description': 'Lyft', 'amount': '7.00' }

def test_create_transaction_with_ten_cents(context):
    transaction = Transaction(
            date='2020-09-14',
            description='Lyft',
            amount='710'
            )
    db.session.add(transaction)
    db.session.commit()
    assert transaction.date == date(2020, 9, 14)
    assert transaction.description == 'Lyft'
    assert transaction.amount == 710
    assert transaction.to_dict() == { 'id': 1, 'date': '2020-09-14', 'description': 'Lyft', 'amount': '7.10' }

def test_unique_transaction(context):
    transaction = Transaction(
            date='2020-09-14',
            description='Lyft',
            amount='700'
            )
    db.session.add(transaction)
    db.session.commit()

    transaction1 = Transaction(
            date='2020-09-14',
            description='Lyft',
            amount='700'
            )
    db.session.add(transaction1)
    with pytest.raises(IntegrityError) as error:
      db.session.commit()

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
