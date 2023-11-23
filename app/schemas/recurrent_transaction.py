from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
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
    timestamp = auto_field(dump_only=True)
