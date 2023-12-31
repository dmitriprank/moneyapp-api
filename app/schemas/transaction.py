from marshmallow import Schema, fields, validate
from marshmallow import ValidationError

from datetime import date
from app.types import TransactionType
from app.models import CategoryModel
from app.schemas.category import CategoryNestedSchema


class TransactionSchema(Schema):
    class Meta:
        fields = ("id", "type", "amount", "category", "description", "date", "timestamp")

    id = fields.Int(dump_only=True)
    type = fields.Enum(TransactionType, by_value=True, required=True)
    amount = fields.Str(required=True)
    category = fields.Nested(CategoryNestedSchema, dump_only=True)
    category_id = fields.Integer(required=True, load_only=True)
    description = fields.String(validate=validate.Length(max=512))
    date = fields.Date(default=date.today())
    timestamp = fields.DateTime(dump_only=True)


class TransactionUpdateSchema(Schema):
    amount = fields.Str()
    category_id = fields.Integer()
    description = fields.String(validate=validate.Length(max=512))
    date = fields.Date()


class TransactionQuerySchema(Schema):
    start_date = fields.Date(data_key='startDate', format='%Y-%m-%d')
    end_date = fields.Date(data_key='endDate', format='%Y-%m-%d')


class TransactionCreateSchema(Schema):
    type = fields.Enum(TransactionType, by_value=True, required=True)
    amount = fields.Str(required=True)
    category_id = fields.Integer(required=True)
    description = fields.String(validate=validate.Length(max=512))
    date = fields.Date(default=date.today())

    def validate_category_id(self, value):
        category = CategoryModel.filter_by(id=value).first()
        if not category:
            raise ValidationError("Invalid category_id")
