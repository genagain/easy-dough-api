import pytest

from app import create_app, db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            # TODO make sure dbs actually drop and create after each test
            # db.session.remove()
            # db.drop_all()
            # db.create_all()
            # import pdb; pdb.set_trace()
            yield client
