import datetime

from db import db
from sqlalchemy import func

from app.types import TransactionType


# TODO: add note field for transaction
class TransactionModel(db.Model):
    __tablename__ = "transaction"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),  nullable=False)
    type = db.Column(db.Enum(TransactionType, name="category_type",
                             values_callable=lambda x: [str(t.value) for t in TransactionType]),
                     nullable=False)
    amount = db.Column(db.DECIMAL(12, 2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),  nullable=False)
    description = db.Column(db.String(512))
    date = db.Column(db.Date, default=datetime.date.today())
    timestamp = db.Column(db.DateTime, server_default=func.now())

    user = db.relationship("UserModel", back_populates="transactions", lazy=True)
    category = db.relationship('CategoryModel', backref="transactions")

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
