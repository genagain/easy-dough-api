from datetime import date
import pytest
from sqlalchemy.exc import IntegrityError

from app import create_app, db
from app.models import User, Transaction

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
    assert transaction.to_dict() == { 'date': '2020-09-14', 'description': 'Lyft', 'amount': '7.00' }

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
    assert transaction.to_dict() == { 'date': '2020-09-14', 'description': 'Lyft', 'amount': '7.10' }

