from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('transactions', __name__, url_prefix='/transactions')

@bp.route('/', methods=['GET'], strict_slashes=False)
@jwt_required
def transactions():
    current_user_email = get_jwt_identity()
    return { 'logged_in_as': current_user_email }, 200
