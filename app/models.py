import re
from flask_bcrypt import generate_password_hash
from sqlalchemy.orm import relationship
from app import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(128), nullable=False)
    lastname = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    banks = relationship('Bank', back_populates='user')

    @classmethod
    def create(cls, firstname, lastname, email, password):
        hashed_password = generate_password_hash(password).decode('utf-8')
        user = cls(
                firstname=firstname,
                lastname=lastname,
                email=email,
                password=hashed_password
                )
        db.session.add(user)
        db.session.commit()
        return user


class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date(), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Integer(), nullable=False)

    __table_args__ = (db.Index('unique_transaction_index', 'date', 'description', 'amount', unique=True),)

    def to_dict(self):
        dollar_amount = str(round(self.amount/100, 2))
        if re.match(r'^\d{0,3},{0,1}\d{0,3}\.\d$', dollar_amount):
            formatted_dollar_amount = f'{dollar_amount}0'
        else:
            formatted_dollar_amount = dollar_amount

        return { 'id': self.id, 'date': self.date.strftime('%Y-%m-%d'), 'description': self.description, 'amount': formatted_dollar_amount }

class Bank(db.Model):
    __tablename__ = "banks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    access_token = db.Column(db.String(255), nullable=False)
    logo = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates="banks")

    __table_args__ = (db.Index('unique_bank_index', 'name', 'user_id', unique=True),)
