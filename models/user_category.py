from db import db
from sqlalchemy import func


class UserCategoryModel(db.Model):
    __tablename__ = "user_category"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),  nullable=False)

    user = db.relationship("UserModel", back_populates="categories", lazy=True)
