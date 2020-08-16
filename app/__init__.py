from flask import Flask, render_template
from .config import Configuration
from .models import db

app = Flask(__name__)
app.config.from_object(Configuration)
db.init_app(app)

@app.route('/')
def main_page():
    return {'some': 'json'}

