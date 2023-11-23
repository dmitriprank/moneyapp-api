from marshmallow import Schema, fields

from app.types import TransactionType


class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    type = fields.Enum(TransactionType, by_value=True, required=True)
    name = fields.Str(required=True)


class CategoryUpdateSchema(Schema):
    type = fields.Enum(TransactionType, by_value=True)
    name = fields.Str()


class CategoryNestedSchema(CategorySchema):
    class Meta:
        exclude = ('type',)


class CategoriesQuerySchema(Schema):
    type = fields.Enum(TransactionType, by_value=True)
