from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from db import db
from app.models import RecurrentTransactionModel
from app.schemas.recurrent_transaction import RecurrentTransactionSchema, RecurrentTransactionUpdateSchema

bp = Blueprint("recurrent_transactions", __name__, description="Operations on recurrent_transactions")


@bp.route("/recurrent_transactions")
class UserRecurrentTransactions(MethodView):
    @jwt_required()
    @bp.response(200, RecurrentTransactionSchema(many=True))
    def get(self):
        user_id = get_jwt_identity()
        recurrent_transactions = (RecurrentTransactionModel.query.filter_by(user_id=user_id)
                                  .order_by(RecurrentTransactionModel.next_transaction.asc()))
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


@bp.route("/recurrent_transactions/<int:rt_id>")
class Transaction(MethodView):
    @jwt_required()
    @bp.response(200, RecurrentTransactionSchema)
    def get(self, rt_id):
        return RecurrentTransactionModel.query.get_or_404(rt_id, description="Recurrent transaction not found")

    @jwt_required()
    @bp.arguments(RecurrentTransactionUpdateSchema, location='json')
    @bp.response(200, RecurrentTransactionSchema)
    def patch(self, upd_rt_data, rt_id):
        recurrent_transaction = RecurrentTransactionModel.query.get(rt_id)
        if not recurrent_transaction:
            return abort(404, message="Recurrent transaction not found")

        recurrent_transaction.update(**upd_rt_data)
        try:
            db.session.add(recurrent_transaction)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error occurred while updating recurrent transaction")

        return recurrent_transaction

    @jwt_required()
    @bp.response(204)
    def delete(self, rt_id):
        recurrent_transaction = RecurrentTransactionModel.query.get_or_404(rt_id)
        if not recurrent_transaction:
            return abort(404, message="Recurrent transaction not found")
        db.session.delete(recurrent_transaction)
        db.session.commit()
