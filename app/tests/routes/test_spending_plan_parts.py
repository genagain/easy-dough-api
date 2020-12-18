import pytest

from app import db
from app.models import User, SpendingPlanPart
from .utils import client, login_test_user

def test_unauthorized_spending_plan_parts(client):
    response = client.get('/spending_plan_parts')
    json_response = response.get_json()
    assert json_response['msg'] == 'Missing Authorization Header'

def test_default_spending_plan_parts(client, login_test_user):
    access_token = login_test_user

    user = User.query.filter_by(email='john@test.com').first()
    spending_plan_part = SpendingPlanPart(
            category='Discretionary Spending',
            label='Spending Money',
            search_term='*',
            expected_amount=0,
            user=user
            )
    db.session.add(spending_plan_part)
    db.session.commit()

    response = client.get('/spending_plan_parts', headers={"Authorization": f"Bearer {access_token}"})
    json_response = response.get_json()
    assert json_response == {
            'discretionarySpending' : {
                'id': 1,
                'label': 'Spending Money',
                'searchTerm': '*',
                'expectedAmount': 0
                }
            }
