from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from db import db
from app.models import RecurrentTransactionModel
from app.schemas.recurrent_transaction import RecurrentTransactionSchema

bp = Blueprint("recurrent_transactions", __name__, description="Operations on recurrent_transactions")


@bp.route("/recurrent_transactions")
class UserRecurrentTransactions(MethodView):
    @jwt_required()
    @bp.response(200, RecurrentTransactionSchema(many=True))
    def get(self):
        user_id = get_jwt_identity()
        recurrent_transactions = (RecurrentTransactionModel.query.filter_by(user_id=user_id)
                                  .order_by(RecurrentTransactionModel.next_transaction.desc()))
        return recurrent_transactions

    @jwt_required()
    @bp.arguments(RecurrentTransactionSchema, location='json')
    @bp.response(201, RecurrentTransactionSchema)
    def post(self, recurrent_transaction_data):
        print('Recurrent transaction data:', recurrent_transaction_data)
        user_id = get_jwt_identity()
        recurrent_transaction = RecurrentTransactionModel(**recurrent_transaction_data, user_id=user_id)
        try:
            db.session.add(recurrent_transaction)
            db.session.commit()
        except SQLAlchemyError as e:
            print(e)
            abort(500, message="Error occurred while creating recurrent transaction")
        return recurrent_transaction_data


# @bp.route("/transactions/<int:transaction_id>")
# class Transaction(MethodView):
#     @jwt_required()
#     @bp.response(200, TransactionSchema)
#     def get(self, transaction_id):
#         return TransactionModel.query.get_or_404(transaction_id, description="Transaction not found")
#
#     @jwt_required()
#     @bp.arguments(TransactionUpdateSchema(partial=True))
#     @bp.response(200, TransactionSchema)
#     def patch(self, upd_transaction_data, transaction_id):
#         transaction = TransactionModel.query.get(transaction_id)
#         if not transaction:
#             return abort(404, message="Transaction not found")
#
#         transaction.update(**upd_transaction_data)
#         try:
#             db.session.add(transaction)
#             db.session.commit()
#         except SQLAlchemyError:
#             abort(500, message="Error occurred while updating transaction")
#
#         return transaction
#
#     @jwt_required()
#     @bp.response(204)
#     def delete(self, transaction_id):
#         transaction = TransactionModel.query.get_or_404(transaction_id)
#         if not transaction:
#             return abort(404, message="Transaction not found")
#         db.session.delete(transaction)
#         db.session.commit()
