from datetime import datetime

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import extract, func

from app import db
from ..models import User, Transaction, SpendingPlanPart

bp = Blueprint('reports', __name__, url_prefix='/reports')

@bp.route('/months', methods=['GET'], strict_slashes=False)
@jwt_required
def months():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    account_ids = [ account.id for bank in user.banks for account in bank.accounts ]

    transactions_unique_months = db.session.query(Transaction).distinct(extract('month', Transaction.date)).all()
    months = list(map(lambda t: t.date.strftime("%B"), transactions_unique_months))
    return { 'months': months }, 200

@bp.route('/generate', methods=['GET'], strict_slashes=False)
@jwt_required
def generate():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    month_name = request.args.get('month')
    month_date = datetime.strptime(month_name, "%B")

    discretionary_spending_part = SpendingPlanPart.query.filter_by(user=user, category='Discretionary Spending').first()
    fixed_costs_parts = SpendingPlanPart.query.filter_by(user=user, category='Fixed Costs').order_by('id').all()
    savings_parts = SpendingPlanPart.query.filter_by(user=user, category='Savings').order_by('id').all()
    investments_parts = SpendingPlanPart.query.filter_by(user=user, category='Investments').order_by('id').all()

    historical_spending = []
    for category in [fixed_costs_parts, savings_parts, investments_parts]:
        for part in category:
            actual_amount_cents = Transaction.query.with_entities(func.sum(Transaction.amount).label("actual_amount")).filter(extract('month', Transaction.date) == month_date.month, Transaction.spending_plan_part == part).first()[0]
            label = part.label
            actual_amount = actual_amount_cents / 100
            expected_amount = part.expected_amount
            difference = round(abs(expected_amount - actual_amount), 2)
            row = {
                    'label': label,
                    'actualAmount': round(actual_amount, 2),
                    'expectedAmount': expected_amount,
                    'difference': difference
            }
            historical_spending.append(row)

    part = discretionary_spending_part
    actual_amount_cents = Transaction.query.with_entities(func.sum(Transaction.amount).label("actual_amount")).filter(extract('month', Transaction.date) == month_date.month, Transaction.spending_plan_part == part).first()[0]
    label = part.label
    actual_amount = actual_amount_cents / 100
    expected_amount = part.expected_amount
    difference = round(abs(expected_amount - actual_amount), 2)
    row = {
        'label': label,
        'actualAmount': round(actual_amount, 2),
        'expectedAmount': expected_amount,
        'difference': difference
    }
    historical_spending.append(row)

    return { 'historticalSpending': historical_spending }, 200
