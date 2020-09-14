from app import db

class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date(), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Integer(), nullable=False)
