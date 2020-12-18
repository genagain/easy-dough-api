from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from ..models import User, SpendingPlanPart

bp = Blueprint('spending_plan_parts', __name__, url_prefix='/spending_plan_parts')

@bp.route('/', methods=['GET'], strict_slashes=False)
@jwt_required
def spending_plan_parts():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    discretionary_spending_part = SpendingPlanPart.query.filter_by(user=user, category='Discretionary Spending').first()
    discretionary_spending = { 'id': discretionary_spending_part.id, 'label': discretionary_spending_part.label, 'searchTerm': discretionary_spending_part.search_term, 'expectedAmount': discretionary_spending_part.expected_amount}
    return { 'discretionarySpending': discretionary_spending}, 200


