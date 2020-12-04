from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm.exc import UnmappedInstanceError

from app import db
from ..models import User, Bank, Account

bp = Blueprint('bank_accounts', __name__, url_prefix='/bank_accounts')

@bp.route('/', methods=['GET'], strict_slashes=False)
@jwt_required
def bank_accounts():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    banks = user.banks

    if banks == []:
        return { 'message': 'No bank accounts have been added yet'}

    banks_response = list(map(lambda bank: { 'id': bank.id,'name': bank.name, 'logo': bank.logo, 'accounts': bank.accounts_to_dict() }, banks))
    return { 'banks': banks_response }, 200

@bp.route('/<int:bank_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required
def delete_bank_account(bank_id):
    try:
        bank = Bank.query.get(bank_id)
        db.session.delete(bank)
        db.session.commit()
    except UnmappedInstanceError:
        return { 'message': 'Cannot delete these bank accounts because they do not exist' }, 501
    return { 'message': 'Bank Accounts successfully deleted' }, 200

