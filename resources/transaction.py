from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError


from db import db
from models import TransactionModel
from schemas import TransactionSchema, TransactionUpdateSchema, PlainTransactionSchema, TransactionQuerySchema

bp = Blueprint("transactions", __name__, description="Operations on transactions")


@bp.route("/transactions")
class UserTransactions(MethodView):
    @jwt_required()
    @bp.arguments(TransactionQuerySchema, location='query', as_kwargs=True)
    @bp.response(200, TransactionSchema(many=True))
    def get(self, **kwargs):
        print(kwargs)
        user_id = get_jwt_identity()
        transactions = TransactionModel.query.filter_by(user_id=user_id)
        return transactions

    @jwt_required()
    @bp.arguments(PlainTransactionSchema)
    @bp.response(201, TransactionSchema)
    def post(self, transaction_data):
        user_id = get_jwt_identity()
        transaction = TransactionModel(**transaction_data, user_id=user_id)
        try:
            db.session.add(transaction)
            db.session.commit()
        except SQLAlchemyError as e:
            print(e)
            abort(500, message="Error occurred while creating transaction")
        return transaction


@bp.route("/transactions/<int:transaction_id>")
class Transaction(MethodView):
    @jwt_required()
    @bp.response(200, TransactionSchema)
    def get(self, transaction_id):
        return TransactionModel.query.get_or_404(transaction_id, description="Transaction not found")

    @jwt_required()
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

    @jwt_required()
    @bp.response(204)
    def delete(self, transaction_id):
        transaction = TransactionModel.query.get_or_404(transaction_id)
        if not transaction:
            return abort(404, message="Transaction not found")
        db.session.delete(transaction)
        db.session.commit()
