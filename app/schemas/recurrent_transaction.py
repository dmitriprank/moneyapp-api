from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field, SQLAlchemyAutoSchema
from app.models import RecurrentTransactionModel


class RecurrentTransactionSchema(SQLAlchemySchema):
    class Meta:
        model = RecurrentTransactionModel

    id = auto_field(dump_only=True)
    timestamp = auto_field(dump_only=True)
