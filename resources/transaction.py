from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TransactionSchema, TransactionUpdateSchema
from models import TransactionModel
from db import db
from sqlalchemy.exc import SQLAlchemyError


bp = Blueprint("transactions", __name__, description="Operations on transactions")


@bp.route("/users/<int:user_id>/transactions")
class UserTransactions(MethodView):
    @bp.response(200, TransactionSchema(many=True))
    def get(self, user_id):
        transactions = TransactionModel.query.filter_by(user_id=user_id)
        return transactions


@bp.route("/transactions")
class Transactions(MethodView):
    @bp.arguments(TransactionSchema)
    @bp.response(201, TransactionSchema)
    def post(self, transaction_data):
        transaction = TransactionModel(**transaction_data)
        try:
            db.session.add(transaction)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error occurred while creating transaction")
        return transaction


@bp.route("/transactions/<string:transaction_id>")
class Transaction(MethodView):
    @bp.response(200, TransactionSchema)
    def get(self, transaction_id):
        return TransactionModel.query.get_or_404(transaction_id, description="Transaction not found")

    @bp.arguments(TransactionUpdateSchema)
    @bp.response(200, TransactionSchema)
    def put(self, upd_transaction_data, transaction_id):
        transaction = TransactionModel.query.get(transaction_id)
        if not transaction:
            return abort(404, message="Transaction not found")

        transaction.update(**upd_transaction_data)
        try:
            db.session.add(transaction)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error occurred while updating transaction")

        return transaction

    @bp.response(204, example={'success': True})
    def delete(self, transaction_id):
        transaction = TransactionModel.query.get(transaction_id)
        if not transaction:
            return abort(404, message="Transaction not found")
        db.session.delete(transaction)
        db.session.commit()
        return {'success': True}
