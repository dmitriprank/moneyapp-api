from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import USERS, DEFAULT_USER_DATA

from random import randint


bp = Blueprint("users", __name__, description="Operations on users")


@bp.route("/users/<string:user_id>")
class User(MethodView):
    def get(self, user_id):
        try:
            return {'user': USERS[user_id]}, 200
        except KeyError:
            abort(404, message="User not found")


@bp.route("/users")
class Users(MethodView):
    def get(self):
        return {'users': USERS}, 200

    def post(self):
        data = request.get_json()
        new_username = data.get('username')
        new_user_data = DEFAULT_USER_DATA.copy()
        new_user_data['username'] = new_username
        user_id = randint(1000000, 9999999)
        USERS[user_id] = new_user_data
        return {'user': USERS[user_id]}, 201
