from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import UserSchema
from models import UserModel
from db import db
from sqlalchemy.exc import SQLAlchemyError


bp = Blueprint("users", __name__, description="Operations on users")


@bp.route("/users/<string:user_id>")
class User(MethodView):
    @bp.response(200, UserSchema)
    def get(self, user_id):
        return UserModel.query.get_or_404(user_id, description="User not found")


@bp.route("/users")
class Users(MethodView):
    @bp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()

    @bp.arguments(UserSchema)
    @bp.response(201, UserSchema)
    def post(self, user_data):
        user = UserModel(**user_data)
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred when inserting the user")

        return user
