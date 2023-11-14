from db import db
from sqlalchemy.event import listens_for
from .user import UserModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


class UserCategoryModel(db.Model):
    __tablename__ = "user_category"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),  nullable=False)

    user = db.relationship("UserModel", back_populates="categories", lazy=True)


@listens_for(UserModel, 'after_insert')
def create_default_categories(mapper, connection, user):
    default_categories = ['Category1', 'Category2', 'Category3']

    category_data = [{'name': category_name, 'user_id': user.id} for category_name in default_categories]

    connection.execute(UserCategoryModel.__table__.insert().values(category_data))
