from flask import Blueprint, request
from flask_jwt_extended import create_access_token

# from flask_bcrypt import generate_password_hash
from flask_bcrypt import check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['POST'])
def login_access_token():
    body = request.json
    email = body['email']
    password = body['password']

    # pw_hash = generate_password_hash('password')
    # TODO add check_password method to User model
    pw_hash = b'$2b$12$nbcxvcyEYBLJoB0FgaBt3ee.pleTJNBJ5vkpccKNhq7fflzkiVyCq'
    if email != 'test@test.com' and check_password_hash(pw_hash, 'password'):
        return { "message": "Bad username or password" }, 401

    access_token = create_access_token(identity=email)
    return {'access_token': access_token}, 200
