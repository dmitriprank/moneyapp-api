from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.hash import pbkdf2_sha256


from db import db
from blocklist import BLOCKLIST
from models import UserModel, TransactionModel
from schemas import UserSchema, PlainUserSchema, TransactionSchema, PlainTransactionSchema


bp = Blueprint("users", __name__, description="Operations on users")


@bp.route("/users/<int:user_id>/transactions")
class UserTransactions(MethodView):
    @jwt_required()
    @bp.response(200, TransactionSchema(many=True))
    def get(self, user_id):
        transactions = TransactionModel.query.filter_by(user_id=user_id)
        return transactions

    @jwt_required()
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
    @jwt_required()
    @bp.response(200, UserSchema)
    def get(self, user_id):
        user_id = get_jwt_identity()
        print(user_id)
        return UserModel.query.get_or_404(user_id, description="User not found")


@bp.route("/users")
class Users(MethodView):
    @bp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()


@bp.route("/register")
class UserRegister(MethodView):
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


@bp.route("/signin")
class UserLogin(MethodView):
    @bp.arguments(PlainUserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.email == user_data["email"]
        ).first()

        if not user:
            abort(404, message="User not found")

        if pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}

        abort(401, message="Invalid credentials.")


@bp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out."}
