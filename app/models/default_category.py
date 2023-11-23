from app.db import db

from app.types import TransactionType

default_categories = {
    "expense": ["Bills", "Car", "Clothes", "Eating out", "Entertainment",
                "Food", "Gifts", "Health", "House", "Pets", "Sports",
                "Taxi", "Toiletry", "Transport"],
    "deposit": ["Deposit", "Salary", "Savings"]
}


class DefaultCategoryModel(db.Model):
    __tablename__ = "default_category"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Enum(TransactionType, name="category_type",
                             values_callable=lambda x: [str(t.value) for t in TransactionType]),
                     nullable=False)
    name = db.Column(db.String(64))


def insert_default_categories():
    for c_type, c_list in default_categories.items():
        for name in c_list:
            db.session.add(DefaultCategoryModel(type=c_type, name=name))
    db.session.commit()
