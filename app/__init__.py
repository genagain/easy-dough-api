from datetime import datetime

from flask import Flask, render_template
from .config import Configuration
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
scheduler = BackgroundScheduler()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Configuration)
    from .routes import auth, dashboard
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    jwt.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    return app
