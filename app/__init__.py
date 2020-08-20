from flask import Flask, render_template
from .config import Configuration
from .models import db
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

from .routes import auth, dashboard

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Configuration)
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    jwt.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    return app
