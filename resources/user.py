from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import USERS, DEFAULT_USER_DATA
from schemas import UserSchema

from random import randint


bp = Blueprint("users", __name__, description="Operations on users")


@bp.route("/users/<string:user_id>")
class User(MethodView):
    @bp.response(200, UserSchema)
    def get(self, user_id):
        try:
            return USERS[user_id]
        except KeyError:
            abort(404, message="User not found")


@bp.route("/users")
class Users(MethodView):
    @bp.response(200, UserSchema(many=True))
    def get(self):
        return USERS

    @bp.arguments(UserSchema)
    @bp.response(201, UserSchema)
    def post(self, user_data):
        new_username = user_data.get('username')
        new_user_data = DEFAULT_USER_DATA.copy()
        new_user_data['username'] = new_username
        user_id = randint(1000000, 9999999)
        USERS[user_id] = new_user_data
        return USERS[user_id]
