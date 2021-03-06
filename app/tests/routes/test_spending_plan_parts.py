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
                'expectedAmount': '0.00'
                }
            }


    response = client.get('/spending_plan_parts', headers={"Authorization": f"Bearer {access_token}"})
    json_response = response.get_json()
    assert json_response['spending_plan_parts'] == expected_response

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
            expected_amount=100000,
            user=user
    )

    electricity = SpendingPlanPart(
            category='Fixed Costs',
            label='Electricity',
            search_term='Electic Company',
            expected_amount=4000,
            user=user
    )

    gas = SpendingPlanPart(
            category='Fixed Costs',
            label='Gas',
            search_term='Gas Company',
            expected_amount=4000,
            user=user
    )

    internet = SpendingPlanPart(
            category='Fixed Costs',
            label='Internet',
            search_term='Internet Provider',
            expected_amount=6000,
            user=user
    )

    groceries = SpendingPlanPart(
            category='Fixed Costs',
            label='Groceries',
            search_term='Grocery Store',
            expected_amount=30000,
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
            'expectedAmount': '1000.00'
          },
          {
            'id': 3,
            'label': 'Electricity',
            'searchTerm': 'Electic Company',
            'expectedAmount': '40.00'
          },
          {
            'id': 4,
            'label': 'Gas',
            'searchTerm': 'Gas Company',
            'expectedAmount': '40.00'
          },
          {
            'id': 5,
            'label': 'Internet',
            'searchTerm': 'Internet Provider',
            'expectedAmount': '60.00'
          },
          {
            'id': 6,
            'label': 'Groceries',
            'searchTerm': 'Grocery Store',
            'expectedAmount': '300.00'
          }
        ],
        'discretionarySpending': {
          'id': 1,
          'label': 'Spending Money',
          'searchTerm': '*',
          'expectedAmount': '0.00'
        }
      }

    response = client.get('/spending_plan_parts', headers={"Authorization": f"Bearer {access_token}"})
    json_response = response.get_json()
    assert json_response['spending_plan_parts'] == expected_response

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
            expected_amount=100000,
            user=user
    )

    electricity = SpendingPlanPart(
            category='Fixed Costs',
            label='Electricity',
            search_term='Electic Company',
            expected_amount=4000,
            user=user
    )

    gas = SpendingPlanPart(
            category='Fixed Costs',
            label='Gas',
            search_term='Gas Company',
            expected_amount=4000,
            user=user
    )

    internet = SpendingPlanPart(
            category='Fixed Costs',
            label='Internet',
            search_term='Internet Provider',
            expected_amount=6000,
            user=user
    )

    groceries = SpendingPlanPart(
            category='Fixed Costs',
            label='Groceries',
            search_term='Grocery Store',
            expected_amount=30000,
            user=user
    )

    savings = SpendingPlanPart(
            category='Savings',
            label='Emergency Fund',
            search_term='Employer',
            expected_amount=80000,
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
            'expectedAmount': '1000.00'
          },
          {
            'id': 3,
            'label': 'Electricity',
            'searchTerm': 'Electic Company',
            'expectedAmount': '40.00'
          },
          {
            'id': 4,
            'label': 'Gas',
            'searchTerm': 'Gas Company',
            'expectedAmount': '40.00'
          },
          {
            'id': 5,
            'label': 'Internet',
            'searchTerm': 'Internet Provider',
            'expectedAmount': '60.00'
          },
          {
            'id': 6,
            'label': 'Groceries',
            'searchTerm': 'Grocery Store',
            'expectedAmount': '300.00'
          }
        ],
        'savings': [
          {
            'id': 7,
            'label': 'Emergency Fund',
            'searchTerm': 'Employer',
            'expectedAmount': '800.00'
          }
        ],
        'discretionarySpending': {
          'id': 1,
          'label': 'Spending Money',
          'searchTerm': '*',
          'expectedAmount': '0.00'
        }
      }

    response = client.get('/spending_plan_parts', headers={"Authorization": f"Bearer {access_token}"})
    json_response = response.get_json()
    assert json_response['spending_plan_parts'] == expected_response

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
            expected_amount=100000,
            user=user
    )

    electricity = SpendingPlanPart(
            category='Fixed Costs',
            label='Electricity',
            search_term='Electic Company',
            expected_amount=4000,
            user=user
    )

    gas = SpendingPlanPart(
            category='Fixed Costs',
            label='Gas',
            search_term='Gas Company',
            expected_amount=4000,
            user=user
    )

    internet = SpendingPlanPart(
            category='Fixed Costs',
            label='Internet',
            search_term='Internet Provider',
            expected_amount=6000,
            user=user
    )

    groceries = SpendingPlanPart(
            category='Fixed Costs',
            label='Groceries',
            search_term='Grocery Store',
            expected_amount=30000,
            user=user
    )

    savings = SpendingPlanPart(
            category='Savings',
            label='Emergency Fund',
            search_term='Employer',
            expected_amount=80000,
            user=user
    )

    investments = SpendingPlanPart(
            category='Investments',
            label='Index Fund',
            search_term='Brokerage Firm',
            expected_amount=70000,
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
            'expectedAmount': '1000.00'
          },
          {
            'id': 3,
            'label': 'Electricity',
            'searchTerm': 'Electic Company',
            'expectedAmount': '40.00'
          },
          {
            'id': 4,
            'label': 'Gas',
            'searchTerm': 'Gas Company',
            'expectedAmount': '40.00'
          },
          {
            'id': 5,
            'label': 'Internet',
            'searchTerm': 'Internet Provider',
            'expectedAmount': '60.00'
          },
          {
            'id': 6,
            'label': 'Groceries',
            'searchTerm': 'Grocery Store',
            'expectedAmount': '300.00'
          }
        ],
        'savings': [
          {
            'id': 7,
            'label': 'Emergency Fund',
            'searchTerm': 'Employer',
            'expectedAmount': '800.00'
          }
        ],
        'investments': [
          {
            'id': 8,
            'label': 'Index Fund',
            'searchTerm': 'Brokerage Firm',
            'expectedAmount': '700.00'
          }
        ],
        'discretionarySpending': {
          'id': 1,
          'label': 'Spending Money',
          'searchTerm': '*',
          'expectedAmount': '0.00'
        }
      }

    response = client.get('/spending_plan_parts', headers={"Authorization": f"Bearer {access_token}"})
    json_response = response.get_json()
    assert json_response['spending_plan_parts'] == expected_response

def test_spending_plan_part_labels(client, login_test_user):
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
            expected_amount=100000,
            user=user
    )

    electricity = SpendingPlanPart(
            category='Fixed Costs',
            label='Electricity',
            search_term='Electic Company',
            expected_amount=4000,
            user=user
    )

    gas = SpendingPlanPart(
            category='Fixed Costs',
            label='Gas',
            search_term='Gas Company',
            expected_amount=4000,
            user=user
    )

    internet = SpendingPlanPart(
            category='Fixed Costs',
            label='Internet',
            search_term='Internet Provider',
            expected_amount=6000,
            user=user
    )

    groceries = SpendingPlanPart(
            category='Fixed Costs',
            label='Groceries',
            search_term='Grocery Store',
            expected_amount=30000,
            user=user
    )

    savings = SpendingPlanPart(
            category='Savings',
            label='Emergency Fund',
            search_term='Employer',
            expected_amount=80000,
            user=user
    )

    investments = SpendingPlanPart(
            category='Investments',
            label='Index Fund',
            search_term='Brokerage Firm',
            expected_amount=70000,
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

    expected_response = [
            'Rent',
            'Electricity',
            'Gas',
            'Internet',
            'Groceries',
            'Emergency Fund',
            'Index Fund',
            'Spending Money'
    ]

    response = client.get('/spending_plan_parts?field=label', headers={"Authorization": f"Bearer {access_token}"})
    json_response = response.get_json()
    assert json_response['spending_plan_part_labels'] == expected_response

def test_spending_plan_part_add(client, login_test_user):
    access_token = login_test_user

    request_body = {
            'category': 'Fixed Costs',
            'label': 'Rent',
            'search_term': 'Property Management',
            'expected_amount': '1000.00'
    }

    response = client.post('/spending_plan_parts/create', headers={"Authorization": f"Bearer {access_token}"}, json=request_body)
    response_body = response.get_json()

    assert response_body['message'] == 'Spending Plan Part successfully created'

    user = User.query.filter_by(email='john@test.com').first()
    added_spending_plan_part = SpendingPlanPart.query.filter_by(category='Fixed Costs', label='Rent').first()

    assert added_spending_plan_part.category == 'Fixed Costs'
    assert added_spending_plan_part.label == 'Rent'
    assert added_spending_plan_part.search_term == 'Property Management'
    assert added_spending_plan_part.expected_amount == 100000
    assert added_spending_plan_part.user == user

def test_spending_plan_part_add_duplicate(client, login_test_user):
    access_token = login_test_user

    user = User.query.filter_by(email='john@test.com').first()

    rent = SpendingPlanPart(
            category='Fixed Costs',
            label='Rent',
            search_term='Property Management Company',
            expected_amount=100000,
            user=user
    )
    db.session.add(rent)
    db.session.commit()

    request_body = {
            'category': 'Fixed Costs',
            'label': 'Rent',
            'search_term': 'Property Management',
            'expected_amount': '1000.00'
    }

    response = client.post('/spending_plan_parts/create', headers={"Authorization": f"Bearer {access_token}"}, json=request_body)
    response_body = response.get_json()

    assert response.status_code == 501
    assert response_body['message'] == 'Cannot create this spending plan part because it already exists'

def test_spending_plan_part_update(client, login_test_user):
    access_token = login_test_user

    user = User.query.filter_by(email='john@test.com').first()

    rent = SpendingPlanPart(
            category='Fixed Costs',
            label='Rent',
            search_term='Property Management Company',
            expected_amount=100000,
            user=user
    )
    db.session.add(rent)
    db.session.commit()

    request_body = {
            'category': 'Fixed Costs',
            'label': 'Rent',
            'search_term': 'New Property Management',
            'expected_amount': '1500.00'
    }

    response = client.put('/spending_plan_parts/1', headers={"Authorization": f"Bearer {access_token}"}, json=request_body)
    response_body = response.get_json()

    assert response_body['message'] == 'Spending Plan Part successfully updated'

    updated_spending_plan_part = SpendingPlanPart.query.get(1)

    assert updated_spending_plan_part.category == 'Fixed Costs'
    assert updated_spending_plan_part.label == 'Rent'
    assert updated_spending_plan_part.search_term == 'New Property Management'
    assert updated_spending_plan_part.expected_amount == 150000
    assert updated_spending_plan_part.user == user

def test_invalid_spending_plan_part_update(client, login_test_user):
    access_token = login_test_user
    request_body = {
            'category': 'Fixed Costs',
            'label': 'Rent',
            'search_term': 'New Property Management',
            'expected_amount': '1500.00'
    }

    response = client.put('/spending_plan_parts/1', headers={"Authorization": f"Bearer {access_token}"}, json=request_body)
    response_body = response.get_json()

    assert response_body['message'] == 'Cannot update this spending plan part because it does not exist'
    assert response.status_code == 501

def test_valid_spending_plan_part_delete(client, login_test_user):
    access_token = login_test_user

    user = User.query.filter_by(email='john@test.com').first()

    rent = SpendingPlanPart(
            category='Fixed Costs',
            label='Rent',
            search_term='Property Management Company',
            expected_amount=100000,
            user=user
    )
    db.session.add(rent)
    db.session.commit()

    response = client.delete('/spending_plan_parts/1', headers={ "Authorization": f"Bearer {access_token}" })
    response_body = response.get_json()

    message = response_body['message']

    assert message == "Spending Plan Part successfully deleted"
    assert response.status_code == 200

    deleted_spending_plan_part = SpendingPlanPart.query.filter_by(category='Fixed Costs', label='Rent').first()
    assert deleted_spending_plan_part == None

def test_invalid_spending_plan_part_delete(client, login_test_user):
    access_token = login_test_user

    response = client.delete('/spending_plan_parts/1', headers={ "Authorization": f"Bearer {access_token}" })
    response_body = response.get_json()

    message = response_body['message']

    assert message == "Cannot delete this spending plan part because it does not exist"
    assert response.status_code == 501
