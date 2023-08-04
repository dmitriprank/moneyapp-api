from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import USERS
from schemas import TransactionSchema, TransactionUpdateSchema

import uuid
import time


bp = Blueprint("transactions", __name__, description="Operations on transactions")


@bp.route("/users/<int:user_id>/transactions")
class UserTransactions(MethodView):
    @bp.response(200, TransactionSchema(many=True))
    def get(self, user_id):
        try:
            user = USERS[user_id]
        except KeyError:
            abort(404, message='User not found.')
        else:
            return user['transactions']

    @bp.arguments(TransactionSchema)
    @bp.response(201, TransactionSchema)
    def post(self, transaction_data, user_id):
        new_transaction = {**transaction_data,
                           'id': uuid.uuid4().hex,
                           'timestamp': int(time.time())}
        try:
            USERS[user_id]['transactions'].append(new_transaction)
        except KeyError:
            abort(404, message="User not found")
        return new_transaction


@bp.route("/users/<int:user_id>/transactions/<string:transaction_id>")
class Transactions(MethodView):
    @bp.response(200, TransactionSchema)
    def get(self, user_id, transaction_id):
        try:
            user = USERS[user_id]
        except KeyError:
            abort(404, message='User not found.')
        else:
            for trans in user['transactions']:
                if trans['id'] == transaction_id:
                    return trans
            abort(404, message='Transaction with that id not found.')

    @bp.arguments(TransactionUpdateSchema)
    @bp.response(200, TransactionSchema)
    def put(self, upd_transaction_data, user_id, transaction_id):
        try:
            user = USERS[user_id]
        except KeyError:
            abort(404, message="User not found.")
        else:
            for idx, trans in enumerate(user['transactions']):
                if trans['id'] == transaction_id:
                    user['transactions'][idx].update(upd_transaction_data)
                    return user['transactions'][idx]
            abort(404, message='Transaction not found.')

    @bp.response(204, example={'success': True})
    def delete(self, user_id, transaction_id):
        try:
            user = USERS[user_id]
        except KeyError:
            abort(404, message='User not found.')
        else:
            for idx, trans in enumerate(user['transactions']):
                if trans['id'] == transaction_id:
                    user['transactions'].pop(idx)
                    return {'success': True}, 204
            abort(404, message='Transaction with that id not found.')
