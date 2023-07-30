from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import USERS

import uuid
import time


bp = Blueprint("transactions", __name__, description="Operations on transactions")


@bp.route("/users/<int:user_id>/transactions")
class UserTransactions(MethodView):
    def get(self, user_id):
        try:
            user = USERS[user_id]
        except KeyError:
            abort(404, message='User not found.')
        else:
            return {'transactions': user['transactions']}, 200

    def post(self, user_id):
        transaction_data = request.get_json()
        new_transaction = {**transaction_data,
                           'id': uuid.uuid4().hex,
                           'timestamp': int(time.time())}
        try:
            USERS[user_id]['transactions'].append(new_transaction)
        except KeyError:
            abort(404, message="User not found")
        return {'transaction': new_transaction}, 201


@bp.route("/users/<int:user_id>/transactions/<string:transaction_id>")
class Transactions(MethodView):
    def get(self, user_id, transaction_id):
        try:
            user = USERS[user_id]
        except KeyError:
            abort(404, message='User not found.')
        else:
            for trans in user['transactions']:
                if trans['id'] == transaction_id:
                    return {'transaction': trans}, 200
            abort(404, message='Transaction with that id not found.')

    def put(self, user_id, transaction_id):
        upd_transaction_data = request.get_json()
        try:
            user = USERS[user_id]
        except KeyError:
            abort(404, message="User not found.")
        else:
            for idx, trans in enumerate(user['transactions']):
                if trans['id'] == transaction_id:
                    user['transactions'][idx].update(upd_transaction_data)
                    return {'transaction': user['transactions'][idx]}, 200
            abort(404, message='Transaction not found.')

    def delete(self, user_id, transaction_id):
        try:
            user = USERS[user_id]
        except KeyError:
            abort(404, message='User not found.')
        else:
            for idx, trans in enumerate(user['transactions']):
                if trans['id'] == transaction_id:
                    user['transactions'].pop(idx)
                    return {'success': True}, 200
            abort(404, message='Transaction with that id not found.')
