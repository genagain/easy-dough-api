import pytest
from sqlalchemy.exc import IntegrityError

from app import create_app, db
from app.models import User

@pytest.fixture
def context():
    app = create_app()
    with app.app_context() as context:
        db.session.remove()
        db.drop_all()
        db.create_all()
        yield context


def test_add_user(context):
    user = User(
            firstname='Jesse',
            lastname='Test',
            email='jesse@test.com',
            password='password'
            )
    db.session.add(user)
    db.session.commit()
    assert user.firstname == 'Jesse'
    assert user.lastname == 'Test'
    assert user.email == 'jesse@test.com'
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
