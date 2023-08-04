from marshmallow import Schema, fields


class UserSchema(Schema):
    user_id = fields.Str(dump_only=True)
    username = fields.Str()
    email = fields.Str()


class TransactionSchema(Schema):
    trans_id = fields.Str(dump_only=True)
    type = fields.Str(required=True)
    amount = fields.Str(required=True)
    category = fields.Str(required=True)
    date = fields.Date()
    timestamp = fields.DateTime(dump_only=True)


class TransactionUpdateSchema(Schema):
    amount = fields.Str()
    category = fields.Str()
    date = fields.Date()
