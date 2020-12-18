from datetime import datetime
import os

from flask import Flask, render_template
from .config import Configuration
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from plaid import Client

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
scheduler = BackgroundScheduler()
PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')
PLAID_ENV = os.getenv('PLAID_ENV', 'sandbox')
plaid_client = Client(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET, environment=PLAID_ENV, api_version='2019-05-29')

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Configuration)
    from .routes import auth, transactions, bank_accounts, spending_plan_parts
    app.register_blueprint(auth.bp)
    app.register_blueprint(transactions.bp)
    app.register_blueprint(bank_accounts.bp)
    app.register_blueprint(spending_plan_parts.bp)
    jwt.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    return app
