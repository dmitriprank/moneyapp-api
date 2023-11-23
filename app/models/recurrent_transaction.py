import datetime

from db import db
from sqlalchemy import func

from app.types import TransactionType, RecurrentFrequency


# TODO: add note field for transaction
class RecurrentTransactionModel(db.Model):
    __tablename__ = "recurrent_transaction"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),  nullable=False)
    type = db.Column(db.Enum(TransactionType, name="transaction_type",
                             values_callable=lambda x: [str(t.value) for t in TransactionType]),
                     nullable=False)
    amount = db.Column(db.DECIMAL(12, 2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),  nullable=False)
    description = db.Column(db.String(512))
    frequency = db.Column(db.Enum(RecurrentFrequency, name="recurrent_frequency",
                                  values_callable=lambda x: [str(t.value) for t in RecurrentFrequency]),
                          nullable=False)
    start_date = db.Column(db.Date, default=datetime.date.today())
    end_date = db.Column(db.Date, nullable=True)
    next_transaction = db.Column(db.Date, default=start_date)

    timestamp = db.Column(db.DateTime, server_default=func.now())

    user = db.relationship("UserModel", back_populates="recurrent_transactions", lazy=True)
    category = db.relationship('CategoryModel', backref="recurrent_transactions")

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
