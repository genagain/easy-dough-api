from flask import Blueprint
from flask_jwt_extended import jwt_required

from app import db
from ..models import Bank, Account

bp = Blueprint('bank_accounts', __name__, url_prefix='/bank_accounts')

@bp.route('/', methods=['GET'], strict_slashes=False)
@jwt_required
def bank_accounts():
    return {}, 501
