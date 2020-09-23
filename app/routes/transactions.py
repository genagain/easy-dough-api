from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models import Transaction

bp = Blueprint('transactions', __name__, url_prefix='/transactions')

@bp.route('/', methods=['GET'], strict_slashes=False)
@jwt_required
def transactions():
    current_user_email = get_jwt_identity()
    if request.args == {}:
        return { 'message': 'Query parameters not found. Please provide dates or a search term in the request' }, 200

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date:
        return { 'message': 'Start date query parameter not found. Please provide a start date' }, 200

    transactions = Transaction.query.filter(Transaction.date.between(start_date, end_date)).all()

    transactions_data = list(map(lambda t: t.to_dict(), transactions))
    return { 'transactions': transactions_data }, 200
