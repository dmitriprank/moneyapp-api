from marshmallow import Schema, fields
from marshmallow import ValidationError

from datetime import date
from app.types import TransactionType
from app.models import CategoryModel


class PlainCategorySchema(Schema):
    id = fields.Int(dump_only=True)
    type = fields.Enum(TransactionType, by_value=True, required=True)
    name = fields.Str(required=True)


class CategorySchema(PlainCategorySchema):
    user_id = fields.Int(required=True)


class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class PlainTransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    type = fields.Enum(TransactionType, by_value=True, required=True)
    amount = fields.Str(required=True)
    category_id = fields.Nested(PlainCategorySchema())
    date = fields.Date(default=date.today())
    timestamp = fields.DateTime(dump_only=True)


class UserSchema(PlainUserSchema):
    transactions = fields.Nested(PlainTransactionSchema(), many=True, dump_only=True)


class TransactionSchema(PlainTransactionSchema):
    user_id = fields.Int(required=True)


class TransactionUpdateSchema(Schema):
    amount = fields.Str()
    category = fields.Str()
    date = fields.Date()


class TransactionQuerySchema(Schema):
    start_date = fields.Date(data_key='startDate', format='%Y-%m-%d')
    end_date = fields.Date(data_key='endDate', format='%Y-%m-%d')


class CategoriesQuerySchema(Schema):
    type = fields.Enum(TransactionType, by_value=True)


class TransactionCreateSchema(Schema):
    type = fields.Enum(TransactionType, by_value=True, required=True)
    amount = fields.Str(required=True)
    category_id = fields.Integer(required=True)
    date = fields.Date(default=date.today())

    def validate_category_id(self, value):
        category = CategoryModel.filter_by(id=value).first()
        if not category:
            raise ValidationError("Invalid category_id")
