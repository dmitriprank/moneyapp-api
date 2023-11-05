from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError


from db import db
from models import TransactionModel
from schemas import TransactionSchema, TransactionUpdateSchema


bp = Blueprint("transactions", __name__, description="Operations on transactions")


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
