from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from app.models import RecurrentTransactionModel


class RecurrentTransactionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RecurrentTransactionModel
        include_fk = True

    id = auto_field(dump_only=True)
    timestamp = auto_field(dump_only=True)
