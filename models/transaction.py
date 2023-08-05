from db import db
from sqlalchemy import func


class TransactionModel(db.Model):
    __tablename__ = "transaction"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),  nullable=False)
    type = db.Column(db.Enum("deposit", "expense", name="transaction_type", create_type=True), nullable=False)
    amount = db.Column(db.DECIMAL(12, 2), nullable=False)
    category = db.Column(db.String(64))
    date = db.Column(db.Date)
    timestamp = db.Column(db.DateTime, server_default=func.now())

    user = db.relationship("UserModel", back_populates="transactions", lazy=True)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
