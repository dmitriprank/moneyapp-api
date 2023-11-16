from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError


from db import db
from models import CategoryModel
from schemas import UserCategorySchema, PlainUserCategorySchema, CategoriesQuerySchema

bp = Blueprint("categories", __name__, description="Operations on categories")


@bp.route("/categories")
class UserCategories(MethodView):
    @jwt_required()
    @bp.arguments(CategoriesQuerySchema, location='query')
    @bp.response(200, UserCategorySchema(many=True))
    def get(self, category_type):
        user_id = get_jwt_identity()
        print(category_type)
        categories = CategoryModel.query.filter_by(user_id=user_id)
        if category_type:
            categories.filter_by(type=category_type)
            print(categories)
        return categories

    @jwt_required()
    @bp.arguments(PlainUserCategorySchema)
    @bp.response(201, UserCategorySchema)
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
    @bp.response(200, UserCategorySchema)
    def get(self, category_id):
        return CategoryModel.query.get_or_404(category_id, description="Category not found")

    # @jwt_required()
    # @bp.arguments(TransactionUpdateSchema)
    # @bp.response(200, TransactionSchema)
    # def put(self, upd_transaction_data, transaction_id):
    #     transaction = TransactionModel.query.get(transaction_id)
    #     if not transaction:
    #         return abort(404, message="Transaction not found")
    #
    #     transaction.update(**upd_transaction_data)
    #     try:
    #         db.session.add(transaction)
    #         db.session.commit()
    #     except SQLAlchemyError:
    #         abort(500, message="Error occurred while updating transaction")
    #
    #     return transaction

    @jwt_required()
    @bp.response(204)
    def delete(self, category_id):
        transaction = CategoryModel.query.get_or_404(category_id)
        if not transaction:
            return abort(404, message="Category not found")
        db.session.delete(transaction)
        db.session.commit()
