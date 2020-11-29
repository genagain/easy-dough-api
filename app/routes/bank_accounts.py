from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

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
