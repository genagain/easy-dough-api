import pytest

from app import db
from app.models import User, SpendingPlanPart
from .utils import client, login_test_user

def test_unauthorized_spending_plan_parts(client):
    response = client.get('/spending_plan_parts')
    json_response = response.get_json()
    assert json_response['msg'] == 'Missing Authorization Header'

# TODO make sure the default spending part is added when the user signs up
def test_default_spending_plan_parts(client, login_test_user):
    access_token = login_test_user

    user = User.query.filter_by(email='john@test.com').first()
    discretionary_spending = SpendingPlanPart(
            category='Discretionary Spending',
            label='Spending Money',
            search_term='*',
            expected_amount=0,
            user=user
            )
    db.session.add(discretionary_spending)
    db.session.commit()
    expected_response = {
            'discretionarySpending' : {
                'id': 1,
                'label': 'Spending Money',
                'searchTerm': '*',
                'expectedAmount': 0
                }
            }


    response = client.get('/spending_plan_parts', headers={"Authorization": f"Bearer {access_token}"})
    json_response = response.get_json()
    assert json_response == expected_response

def test_fixed_costs_spending_plan_parts(client, login_test_user):
    access_token = login_test_user

    user = User.query.filter_by(email='john@test.com').first()
    discretionary_spending = SpendingPlanPart(
            category='Discretionary Spending',
            label='Spending Money',
            search_term='*',
            expected_amount=0,
            user=user
            )

    rent = SpendingPlanPart(
            category='Fixed Costs',
            label='Rent',
            search_term='Property Management Company',
            expected_amount=1000,
            user=user
    )

    electricity = SpendingPlanPart(
            category='Fixed Costs',
            label='Electricity',
            search_term='Electic Company',
            expected_amount=40,
            user=user
    )

    gas = SpendingPlanPart(
            category='Fixed Costs',
            label='Gas',
            search_term='Gas Company',
            expected_amount=40,
            user=user
    )

    internet = SpendingPlanPart(
            category='Fixed Costs',
            label='Internet',
            search_term='Internet Provider',
            expected_amount=60,
            user=user
    )

    groceries = SpendingPlanPart(
            category='Fixed Costs',
            label='Groceries',
            search_term='Grocery Store',
            expected_amount=300,
            user=user
    )

    db.session.add(discretionary_spending)
    db.session.add(rent)
    db.session.add(electricity)
    db.session.add(gas)
    db.session.add(internet)
    db.session.add(groceries)
    db.session.commit()

    expected_response = {
        'fixedCosts': [
          {
            'id': 2,
            'label': 'Rent',
            'searchTerm': 'Property Management Company',
            'expectedAmount': 1000
          },
          {
            'id': 3,
            'label': 'Electricity',
            'searchTerm': 'Electic Company',
            'expectedAmount': 40
          },
          {
            'id': 4,
            'label': 'Gas',
            'searchTerm': 'Gas Company',
            'expectedAmount': 40
          },
          {
            'id': 5,
            'label': 'Internet',
            'searchTerm': 'Internet Provider',
            'expectedAmount': 60
          },
          {
            'id': 6,
            'label': 'Groceries',
            'searchTerm': 'Grocery Store',
            'expectedAmount': 300
          }
        ],
        'discretionarySpending': {
          'id': 1,
          'label': 'Spending Money',
          'searchTerm': '*',
          'expectedAmount': 0
        }
      }

    response = client.get('/spending_plan_parts', headers={"Authorization": f"Bearer {access_token}"})
    json_response = response.get_json()
    assert json_response == expected_response

def test_savings_spending_plan_parts(client, login_test_user):
    access_token = login_test_user

    user = User.query.filter_by(email='john@test.com').first()
    discretionary_spending = SpendingPlanPart(
            category='Discretionary Spending',
            label='Spending Money',
            search_term='*',
            expected_amount=0,
            user=user
            )

    rent = SpendingPlanPart(
            category='Fixed Costs',
            label='Rent',
            search_term='Property Management Company',
            expected_amount=1000,
            user=user
    )

    electricity = SpendingPlanPart(
            category='Fixed Costs',
            label='Electricity',
            search_term='Electic Company',
            expected_amount=40,
            user=user
    )

    gas = SpendingPlanPart(
            category='Fixed Costs',
            label='Gas',
            search_term='Gas Company',
            expected_amount=40,
            user=user
    )

    internet = SpendingPlanPart(
            category='Fixed Costs',
            label='Internet',
            search_term='Internet Provider',
            expected_amount=60,
            user=user
    )

    groceries = SpendingPlanPart(
            category='Fixed Costs',
            label='Groceries',
            search_term='Grocery Store',
            expected_amount=300,
            user=user
    )

    savings = SpendingPlanPart(
            category='Savings',
            label='Emergency Fund',
            search_term='Employer',
            expected_amount=800,
            user=user
    )

    db.session.add(discretionary_spending)
    db.session.add(rent)
    db.session.add(electricity)
    db.session.add(gas)
    db.session.add(internet)
    db.session.add(groceries)
    db.session.add(savings)
    db.session.commit()

    expected_response = {
        'fixedCosts': [
          {
            'id': 2,
            'label': 'Rent',
            'searchTerm': 'Property Management Company',
            'expectedAmount': 1000
          },
          {
            'id': 3,
            'label': 'Electricity',
            'searchTerm': 'Electic Company',
            'expectedAmount': 40
          },
          {
            'id': 4,
            'label': 'Gas',
            'searchTerm': 'Gas Company',
            'expectedAmount': 40
          },
          {
            'id': 5,
            'label': 'Internet',
            'searchTerm': 'Internet Provider',
            'expectedAmount': 60
          },
          {
            'id': 6,
            'label': 'Groceries',
            'searchTerm': 'Grocery Store',
            'expectedAmount': 300
          }
        ],
        'savings': [
          {
            'id': 7,
            'label': 'Emergency Fund',
            'searchTerm': 'Employer',
            'expectedAmount': 800
          }
        ],
        'discretionarySpending': {
          'id': 1,
          'label': 'Spending Money',
          'searchTerm': '*',
          'expectedAmount': 0
        }
      }

    response = client.get('/spending_plan_parts', headers={"Authorization": f"Bearer {access_token}"})
    json_response = response.get_json()
    assert json_response == expected_response

def test_investments_spending_plan_parts(client, login_test_user):
    access_token = login_test_user

    user = User.query.filter_by(email='john@test.com').first()
    discretionary_spending = SpendingPlanPart(
            category='Discretionary Spending',
            label='Spending Money',
            search_term='*',
            expected_amount=0,
            user=user
            )

    rent = SpendingPlanPart(
            category='Fixed Costs',
            label='Rent',
            search_term='Property Management Company',
            expected_amount=1000,
            user=user
    )

    electricity = SpendingPlanPart(
            category='Fixed Costs',
            label='Electricity',
            search_term='Electic Company',
            expected_amount=40,
            user=user
    )

    gas = SpendingPlanPart(
            category='Fixed Costs',
            label='Gas',
            search_term='Gas Company',
            expected_amount=40,
            user=user
    )

    internet = SpendingPlanPart(
            category='Fixed Costs',
            label='Internet',
            search_term='Internet Provider',
            expected_amount=60,
            user=user
    )

    groceries = SpendingPlanPart(
            category='Fixed Costs',
            label='Groceries',
            search_term='Grocery Store',
            expected_amount=300,
            user=user
    )

    savings = SpendingPlanPart(
            category='Savings',
            label='Emergency Fund',
            search_term='Employer',
            expected_amount=800,
            user=user
    )

    investments = SpendingPlanPart(
            category='Investments',
            label='Index Fund',
            search_term='Brokerage Firm',
            expected_amount=700,
            user=user
    )

    db.session.add(discretionary_spending)
    db.session.add(rent)
    db.session.add(electricity)
    db.session.add(gas)
    db.session.add(internet)
    db.session.add(groceries)
    db.session.add(savings)
    db.session.add(investments)
    db.session.commit()

    expected_response = {
        'fixedCosts': [
          {
            'id': 2,
            'label': 'Rent',
            'searchTerm': 'Property Management Company',
            'expectedAmount': 1000
          },
          {
            'id': 3,
            'label': 'Electricity',
            'searchTerm': 'Electic Company',
            'expectedAmount': 40
          },
          {
            'id': 4,
            'label': 'Gas',
            'searchTerm': 'Gas Company',
            'expectedAmount': 40
          },
          {
            'id': 5,
            'label': 'Internet',
            'searchTerm': 'Internet Provider',
            'expectedAmount': 60
          },
          {
            'id': 6,
            'label': 'Groceries',
            'searchTerm': 'Grocery Store',
            'expectedAmount': 300
          }
        ],
        'savings': [
          {
            'id': 7,
            'label': 'Emergency Fund',
            'searchTerm': 'Employer',
            'expectedAmount': 800
          }
        ],
        'investments': [
          {
            'id': 8,
            'label': 'Index Fund',
            'searchTerm': 'Brokerage Firm',
            'expectedAmount': 700
          }
        ],
        'discretionarySpending': {
          'id': 1,
          'label': 'Spending Money',
          'searchTerm': '*',
          'expectedAmount': 0
        }
      }

    response = client.get('/spending_plan_parts', headers={"Authorization": f"Bearer {access_token}"})
    json_response = response.get_json()
    assert json_response == expected_response
