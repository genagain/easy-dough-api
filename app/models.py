import re
from app import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(128), nullable=False)
    lastname = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date(), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Integer(), nullable=False)

    __table_args__ = (db.Index('unique_transaction_index', 'date', 'description', 'amount', unique=True),)

    def to_dict(self):
        row = self.__dict__
        dollar_amount = str(round(self.amount/100, 2))
        if re.match(r'^\d{0,3},{0,1}\d{0,3}\.\d$', dollar_amount):
            formatted_dollar_amount = f'{dollar_amount}0'
        else:
            formatted_dollar_amount = dollar_amount

        return { 'date': self.date.strftime('%Y-%m-%d'), 'description': self.description, 'amount': formatted_dollar_amount }
