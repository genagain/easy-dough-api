import pytest

from app.models import db
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
