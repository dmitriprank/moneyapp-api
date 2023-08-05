from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import UserSchema, PlainUserSchema, TransactionSchema, PlainTransactionSchema
from models import UserModel, TransactionModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.hash import pbkdf2_sha256


bp = Blueprint("users", __name__, description="Operations on users")


@bp.route("/users/<int:user_id>/transactions")
class UserTransactions(MethodView):
    @bp.response(200, TransactionSchema(many=True))
    def get(self, user_id):
        transactions = TransactionModel.query.filter_by(user_id=user_id)
        return transactions

    @bp.arguments(PlainTransactionSchema)
    @bp.response(201, TransactionSchema)
    def post(self, transaction_data, user_id):
        transaction = TransactionModel(**transaction_data, user_id=user_id)
        try:
            db.session.add(transaction)

            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error occurred while creating transaction")
        return transaction


@bp.route("/users/<int:user_id>")
class User(MethodView):
    @bp.response(200, UserSchema)
    def get(self, user_id):
        return UserModel.query.get_or_404(user_id, description="User not found")


@bp.route("/users")
class Users(MethodView):
    @bp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()


@bp.route("/register")
class RegisterUser(MethodView):
    @bp.arguments(PlainUserSchema)
    @bp.response(201, UserSchema)
    def post(self, user_data):
        user = UserModel(
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(409, message="User with such email already exists")
        except SQLAlchemyError:
            abort(500, message="An error occurred when inserting the user")

        return user
