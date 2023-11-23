from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from app.models import RecurrentTransactionModel


class RecurrentTransactionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RecurrentTransactionModel

    id = auto_field(dump_only=True)
    timestamp = auto_field(dump_only=True)
