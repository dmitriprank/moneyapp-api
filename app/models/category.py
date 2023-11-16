from db import db
from sqlalchemy.event import listens_for
from .user import UserModel
from .default_category import DefaultCategoryModel
from app.types import TransactionType


class CategoryModel(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # type = db.Column(db.Enum(TransactionType, name="category_type", create_type=True), nullable=False)
    type = db.Column(db.Enum(*[e.value for e in TransactionType], name="category_type", create_type=True),
                     nullable=False)
    name = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),  nullable=False)

    user = db.relationship("UserModel", back_populates="categories", lazy=True)


@listens_for(UserModel, 'after_insert')
def create_default_categories(mapper, connection, user):
    default_categories = DefaultCategoryModel.query.all()

    category_data = [{'type': cat.type, 'name': cat.name, 'user_id': user.id}
                     for cat in default_categories]

    connection.execute(CategoryModel.__table__.insert().values(category_data))
