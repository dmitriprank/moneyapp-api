from marshmallow import Schema, fields


class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class PlainTransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    type = fields.Str(required=True)
    amount = fields.Str(required=True)
    category = fields.Str(required=True)
    date = fields.Date()
    timestamp = fields.DateTime(dump_only=True)


class UserSchema(PlainUserSchema):
    transactions = fields.Nested(PlainTransactionSchema(), many=True, dump_only=True)


class TransactionSchema(PlainTransactionSchema):
    user_id = fields.Int(required=True)
    user = fields.Nested(PlainUserSchema(), dump_only=True)


class TransactionUpdateSchema(Schema):
    amount = fields.Str()
    category = fields.Str()
    date = fields.Date()
