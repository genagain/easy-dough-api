from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from app import db
from ..models import User, Transaction, SpendingPlanPart

bp = Blueprint('transactions', __name__, url_prefix='/transactions')

@bp.route('/', methods=['GET'], strict_slashes=False)
@jwt_required
def transactions():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    valid_query_parameters = ['start_date', 'end_date', 'search_term']
    extra_query_parameters = set(request.args.keys()) - set(valid_query_parameters)

    if request.args == {} or extra_query_parameters:
        return { 'message': 'Query parameters not found. Please provide both a start date and end date and optionally a search term in the request' }, 200

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not (start_date and end_date):
        return { 'message': 'start_date and end_date query parameters not found. Please provide both a start date and end date' }, 200

    account_ids = [ account.id for bank in user.banks for account in bank.accounts ]

    search_term = request.args.get('search_term')
    if not search_term:
        transactions = Transaction.query.filter(Transaction.date.between(start_date, end_date), Transaction.account_id.in_(account_ids)).order_by(Transaction.date.desc(), Transaction.id.desc()).all()
    else:
        search_clause = f"%{search_term}%"
        transactions = Transaction.query.filter(Transaction.date.between(start_date, end_date), Transaction.account_id.in_(account_ids)).filter(Transaction.description.ilike(search_clause)).order_by(Transaction.date.desc(), Transaction.id.desc()).all()

    month_transactions = {}
    for transaction in transactions:
        month = transaction.date.strftime('%B')
        if month not in month_transactions:
            month_transactions[month] = [ transaction.to_dict() ]
        else:
            month_transactions[month].append(transaction.to_dict())

    response_body = [ { 'month': month, 'transactions': transactions} for month, transactions in month_transactions.items()]
    return jsonify(response_body), 200

@bp.route('/create', methods=['POST'], strict_slashes=False)
@jwt_required
def add_transaction():
    if request.mimetype != 'application/json':
        return { "message": "Invalid format: body must be JSON" }, 501

    body = request.json
    required_fields =  ['date', 'description', 'amount', 'label']
    if not set(body.keys()) == set(required_fields):
        return { "message": "Invalid format: body must contain date, description and amount" }, 501

    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    date = body['date']
    description = body['description']
    amount = body['amount'].replace('.', '')
    label = body['label']

    try:
        # TODO figure out a way for the user to specify which bank account they created transaction should be associated with
        account = user.banks[0].accounts[0]
        spending_plan_part = SpendingPlanPart.query.filter_by(label=label, user=user).first()
        transaction = Transaction(date=date, description=description, amount=amount, account=account, spending_plan_part=spending_plan_part)
        db.session.add(transaction)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return { 'message': 'Cannot create this transaction because it already exists' }, 501

    return { 'message': 'Transaction successfully created' }, 200

@bp.route('/<int:transaction_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required
def delete_transaction(transaction_id):
    try:
        transaction = Transaction.query.get(transaction_id)
        db.session.delete(transaction)
        db.session.commit()
    except UnmappedInstanceError:
        return { 'message': 'Cannot delete this transaction because it does not exist' }, 501

    return { 'message': 'Transaction successfully deleted' }, 200

@bp.route('/<int:transaction_id>', methods=['PUT'], strict_slashes=False)
@jwt_required
def update_transaction(transaction_id):
    if request.mimetype != 'application/json':
        return { "message": "Invalid format: body must be JSON" }, 501

    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    transaction = Transaction.query.get(transaction_id)
    body = request.json

    required_fields =  ['date', 'description', 'amount', 'label']
    if not set(body.keys()) == set(required_fields):
        return { "message": "Invalid format: body must contain date, description and amount" }, 501

    date = body['date']
    description = body['description']
    label = body['label']
    amount = int(body['amount'].replace('.', ''))

    try:
        spending_plan_part = SpendingPlanPart.query.filter_by(label=label, user=user).first()
        transaction.date = date
        transaction.description = description
        transaction.amount = amount
        transaction.spending_plan_part = spending_plan_part
        db.session.commit()

        return { 'message': 'Transaction successfully updated' }, 200
    except AttributeError:
        return { 'message': 'Cannot update this transaction because it does not exist' }, 501
