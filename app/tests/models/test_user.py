import pytest
from sqlalchemy.exc import IntegrityError

from app import db
from app.models.user import User

from .utils import context

def test_add_user(context):
    user = User(
            firstname='Test',
            lastname='User',
            email='test@test.com',
            password='password'
            )
    db.session.add(user)
    db.session.commit()
    assert user.firstname == 'Test'
    assert user.lastname == 'User'
    assert user.email == 'test@test.com'
    assert user.password == 'password'

def test_unique_email(context):
    user = User(
            firstname='Test',
            lastname='User',
            email='test@test.com',
            password='password'
            )
    db.session.add(user)
    db.session.commit()

    user1 = User(
            firstname='John',
            lastname='Doe',
            email='test@test.com',
            password='test'
            )
    db.session.add(user1)
    with pytest.raises(IntegrityError) as error:
      db.session.commit()
