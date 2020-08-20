import os

class Configuration():
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['TEST_DATABASE_URL']  if os.environ['FLASK_ENV'] == 'test' else  os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
