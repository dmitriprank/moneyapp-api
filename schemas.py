from marshmallow import Schema, fields


class UserSchema(Schema):
    user_id = fields.Str()
    username = fields.Str()


class TransactionSchema(Schema):
    id = fields.Str(dump_only=True)
    type = fields.Str()
    amount = fields.Str()
    category = fields.Str()
    timestamp = fields.DateTime()
