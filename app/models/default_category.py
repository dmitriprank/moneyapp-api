from db import db
from sqlalchemy import event

default_categories = {
    "expense": ["Bills", "Car", "Clothes", "Eating out", "Entertainment",
                "Food", "Gifts", "Health", "House", "Pets", "Sports",
                "Taxi", "Toiletry", "Transport"],
    "deposit": ["Deposit", "Salary", "Savings"]
}


class DefaultCategoryModel(db.Model):
    __tablename__ = "default_category"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Enum("deposit", "expense", name="category_type", create_type=True), nullable=False)
    name = db.Column(db.String(64))


@event.listens_for(DefaultCategoryModel.__table__, 'after_configured')
def insert_default_categories(*args, **kwargs):
    for c_type, c_list in default_categories.items():
        for name in c_list:
            db.session.add(DefaultCategoryModel(type=c_type, name=name))
    db.session.commit()
