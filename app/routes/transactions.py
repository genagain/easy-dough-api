from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models import Transaction

bp = Blueprint('transactions', __name__, url_prefix='/transactions')

@bp.route('/', methods=['GET'], strict_slashes=False)
@jwt_required
def transactions():
    current_user_email = get_jwt_identity()
    valid_query_parameters = ['start_date', 'end_date', 'search_term']
    extra_query_parameters = set(request.args.keys()) - set(valid_query_parameters)

    if request.args == {} or extra_query_parameters:
        return { 'message': 'Query parameters not found. Please provide both a start date and end date and optionally a search term in the request' }, 200

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not (start_date and end_date):
        return { 'message': 'start_date and end_date query parameters not found. Please provide both a start date and end date' }, 200

    search_term = request.args.get('search_term')
    if not search_term:
        transactions = Transaction.query.filter(Transaction.date.between(start_date, end_date)).order_by(Transaction.date.desc()).all()
    else:
        search_clause = f"%{search_term}%"
        transactions = Transaction.query.filter(Transaction.date.between(start_date, end_date)).filter(Transaction.description.ilike(search_clause)).order_by(Transaction.date.desc()).all()

# TODO remove this and update tests accordingly
#     if transactions == []:
        # return { 'message': 'No transactions were found that matched the provided date range or search term' }

    month_transactions = {}
    for transaction in transactions:
        month = transaction.date.strftime('%B')
        if month not in month_transactions:
            month_transactions[month] = [ transaction.to_dict() ]
        else:
            month_transactions[month].append(transaction.to_dict())

    response_body = [ { 'month': month, 'transactions': transactions} for month, transactions in month_transactions.items()]
    return jsonify(response_body), 200
