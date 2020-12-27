from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError

from app import db
from ..models import User, SpendingPlanPart

bp = Blueprint('spending_plan_parts', __name__, url_prefix='/spending_plan_parts')

@bp.route('/', methods=['GET'], strict_slashes=False)
@jwt_required
def spending_plan_parts():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    discretionary_spending_part = SpendingPlanPart.query.filter_by(user=user, category='Discretionary Spending').first()
    discretionary_spending = discretionary_spending_part.to_dict()

    fixed_costs_parts = SpendingPlanPart.query.filter_by(user=user, category='Fixed Costs').order_by('id').all()
    fixed_costs = list(map(lambda part: part.to_dict(), fixed_costs_parts))

    savings_parts = SpendingPlanPart.query.filter_by(user=user, category='Savings').order_by('id').all()
    savings = list(map(lambda part: part.to_dict(), savings_parts))

    investments_parts = SpendingPlanPart.query.filter_by(user=user, category='Investments').order_by('id').all()
    investments = list(map(lambda part: part.to_dict(), investments_parts))

    spending_plan = { 'fixedCosts': fixed_costs, 'savings': savings, 'investments': investments, 'discretionarySpending': discretionary_spending }

    response = [(category, parts) for category, parts in spending_plan.items() if parts != []]

    return { 'spending_plan_parts': dict(response) }, 200


@bp.route('/create', methods=['POST'], strict_slashes=False)
@jwt_required
def create_spending_plan_parts():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    body = request.json

    category = body['category']
    label = body['label']
    search_term = body['search_term']
    expected_amount = int(body['expected_amount'].replace('.', ''))

    try:
        spending_plan_part = SpendingPlanPart(category=category, label=label, search_term=search_term, expected_amount=expected_amount, user=user)

        db.session.add(spending_plan_part)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return { 'message': 'Cannot create this spending plan part because it already exists' }, 501

    return { 'message': 'Spending Plan Part successfully created' }, 200


@bp.route('/<int:spending_plan_part_id>', methods=['PUT'], strict_slashes=False)
@jwt_required
def update_spending_plan_part(spending_plan_part_id):
    spending_plan_part = SpendingPlanPart.query.get(spending_plan_part_id)

    body = request.json

    label = body['label']
    search_term = body['search_term']
    expected_amount = int(body['expected_amount'].replace('.', ''))

    spending_plan_part.label = label
    spending_plan_part.search_term = search_term
    spending_plan_part.expected_amount = expected_amount
    db.session.commit()

    return { 'message': 'Spending Plan Part successfully updated' }, 200
