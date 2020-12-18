import re
from flask_bcrypt import generate_password_hash
from sqlalchemy.orm import relationship, validates
from app import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(128), nullable=False)
    lastname = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    banks = relationship('Bank', back_populates='user')
    spending_plan_parts = relationship('SpendingPlanPart', back_populates='user')

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
    # TODO consider changing this to plaid_access_token
    access_token = db.Column(db.String(255), nullable=False)
    logo = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates="banks")
    accounts = relationship('Account', cascade="all,delete-orphan", back_populates="bank")

    __table_args__ = (db.Index('unique_bank_index', 'name', 'user_id', unique=True),)

    def accounts_to_dict(self):
        return list(map(lambda account: account.to_dict(), self.accounts))

class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plaid_account_id = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(128), nullable=False)
    bank_id = db.Column(db.Integer, db.ForeignKey('banks.id'), nullable=False)
    bank = relationship('Bank', back_populates="accounts")

    def to_dict(self):
        return {'name': self.name, 'type': self.type.capitalize() }

class SpendingPlanPart(db.Model):
    __tablename__ = "spending_plan_parts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(128), nullable=False)
    label = db.Column(db.String(255), nullable=False)
    search_term = db.Column(db.String(255), nullable=False)
    expected_amount = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates="spending_plan_parts")

    __table_args__ = (db.Index('unique_spending_plan_parts_index', 'category', 'label', 'user_id', unique=True),)

    @validates('category')
    def validate_category(self, attribute, category):
        if category not in ['Fixed Costs', 'Savings', 'Investments', 'Discretionary Spending']:
            raise ValueError("category must be one the following: 'Fixed Costs', 'Savings', 'Investments', 'Discretionary Spending'")
        return category
