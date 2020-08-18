from flask import Blueprint, request
from flask_jwt_extended import create_access_token

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['POST'])
def login_access_token():
    body = request.json
    email = body['email']
    password = body['password']

    if email != 'test@test.com' and password != 'password':
        return { "message": "Bad username or password" }, 401

    access_token = create_access_token(identity=email)
    return {'access_token': access_token}, 200
