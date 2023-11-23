from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field, SQLAlchemySchema
from marshmallow import fields

from app.models import RecurrentTransactionModel
from app.types import TransactionType, RecurrentFrequency
from app.schemas.category import CategoryNestedSchema


class RecurrentTransactionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RecurrentTransactionModel
        include_fk = True
        exclude = ['user_id']

    id = auto_field(dump_only=True)
    category_id = fields.Integer(required=True, load_only=True)
    category = fields.Nested(CategoryNestedSchema, dump_only=True)
    type = fields.Enum(TransactionType, by_value=True, required=True)
    frequency = fields.Enum(RecurrentFrequency, by_value=True, required=True)
    next_transaction = auto_field(dump_only=True)
    timestamp = auto_field(dump_only=True)


class RecurrentTransactionUpdateSchema(SQLAlchemySchema):
    type = auto_field()
    amount = auto_field()
    category_id = auto_field()
    description = auto_field()
    frequency = auto_field()
    start_date = auto_field()
    end_date = auto_field()
    next_transaction = auto_field()
