from flask import Flask, render_template
from .config import Configuration
from .models import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

from .routes import auth, dashboard

app = Flask(__name__)
app.config.from_object(Configuration)
app.register_blueprint(auth.bp)
app.register_blueprint(dashboard.bp)
jwt = JWTManager(app)
Bcrypt().init_app(app)
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def main_page():
    return {'some': 'json'}
