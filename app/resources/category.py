from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from db import db
from app.models import CategoryModel
from schemas import CategorySchema, CategorySchema, CategoriesQuerySchema, PartialCategorySchema

bp = Blueprint("categories", __name__, description="Operations on categories")


@bp.route("/categories")
class UserCategories(MethodView):
    @jwt_required()
    @bp.arguments(CategoriesQuerySchema, location='query', as_kwargs=True)
    @bp.response(200, CategorySchema(many=True))
    def get(self, **kwargs):
        user_id = get_jwt_identity()
        category_type = kwargs.get("type")
        print(category_type, type(category_type))
        categories = CategoryModel.query.filter(CategoryModel.user_id == user_id)
        if category_type:
            categories = categories.filter(CategoryModel.type == category_type.value)
        print(categories)
        return categories

    @jwt_required()
    @bp.arguments(CategorySchema)
    @bp.response(201, CategorySchema)
    def post(self, category_data):
        user_id = get_jwt_identity()
        category = CategoryModel(**category_data, user_id=user_id)
        try:
            db.session.add(category)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error occurred while creating category")
        return category


@bp.route("/categories/<int:category_id>")
class Categories(MethodView):
    @jwt_required()
    @bp.response(200, CategorySchema)
    def get(self, category_id):
        return CategoryModel.query.get_or_404(category_id, description="Category not found")

    @jwt_required()
    @bp.arguments(PartialCategorySchema)
    @bp.response(200, CategorySchema)
    def patch(self, category_data, category_id):
        category = CategoryModel.query.get(category_id)
        if not category_id:
            return abort(404, message="Category not found")

        category.update(**category_data)
        try:
            db.session.add(category)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error occurred while updating category")

        return category

    @jwt_required()
    @bp.response(204)
    def delete(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)
        if not category:
            return abort(404, message="Category not found")
        db.session.delete(category)
        db.session.commit()
