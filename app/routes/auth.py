from flask import Blueprint, request
from flask_jwt_extended import create_access_token

from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup', methods=['POST'])
def signup():
    if request.mimetype != 'application/json':
        return { "message": "Invalid format: body must be JSON" }, 501

    body = request.json

    required_fields =  ['firstname', 'lastname', 'email', 'password']
    if not set(body.keys()) == set(required_fields):
        return { "message": "Invalid body: body must contain firstname, lastname, email and password" }, 501
    try:
        hashed_password = generate_password_hash(body['password']).decode('utf-8')
        user = User(
                firstname=body['firstname'],
                lastname=body['lastname'],
                email=body['email'],
                password=hashed_password
                )
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return { 'message': f"A user with the email {body['email']} already exists" }, 501

    return { 'message': "Successfully created a new user"}, 200

@bp.route('/login', methods=['POST'])
def login_access_token():
    if request.mimetype != 'application/json':
        return { "message": "Invalid format: body must be JSON" }, 501

    body = request.json
    if not (body.get('email') and body.get('password')):
        return { "message": "Invalid body: body must contain email and password" }, 501

    email = body['email']
    password = body['password']

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return { "message": "Bad email or password" }, 401

    access_token = create_access_token(identity=email)
    return {'access_token': access_token}, 200
