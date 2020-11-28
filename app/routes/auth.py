from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from plaid import Client

from app import db
from app.models import User, Bank

## TODO Move all of this to the app init file
import os
PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')
PLAID_ENV = os.getenv('PLAID_ENV', 'sandbox')
client = Client(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET, environment=PLAID_ENV, api_version='2019-05-29')

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
        User.create(
                firstname=body['firstname'],
                lastname=body['lastname'],
                email=body['email'],
                password=body['password']
                )
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


@bp.route('/create_link_token', methods=['GET'])
@jwt_required
def create_link_token():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    client_user_id = str(user.id)

    response = client.LinkToken.create({
        'user': {
            'client_user_id': client_user_id
        },
        'products': ["transactions"],
        'client_name': "My App",
        'country_codes': ['US'],
        'language': 'en',
        'webhook': 'https://sample.webhook.com'
    })

    link_token = response['link_token']

    return response, 200

@bp.route('/exchange_public_token', methods=['POST'])
@jwt_required
def exchange_public_token():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    body = request.json
    public_token = body['public_token']
    exchange_response = client.Item.public_token.exchange(public_token)
    access_token = exchange_response['access_token']

    # TODO create bank account with access token
    item_response = client.Item.get(access_token)
    item = item_response['item']
    institution_id = item['institution_id']
    institution_response = client.Institutions.get_by_id(institution_id, { 'include_optional_metadata': True})
    institution = institution_response['institution']
    bank_name = institution['name']
    bank_logo = institution['logo']

    # TODO create a class method maybe
    bank = Bank(name=bank_name, logo=bank_logo, access_token=access_token, user=user)
    db.session.add(bank)
    db.session.commit()

    # TODO associate the bank and bank accounts with the user
    accounts_response = client.Accounts.get(access_token)
    accounts = accounts_response['accounts']
    print(list(map(lambda account: { 'account_id': account['account_id'], 'name': account['name'], 'type': account['subtype'] }, accounts)))

    return { 'message': f'Successfully added {bank_name}' }, 200
