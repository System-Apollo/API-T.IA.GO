from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(dump_only=True)
    last_name = fields.String(dump_only=True)
    username = fields.String(dump_only=True)
    company = fields.String(dump_only=True)
    email = fields.String(dump_only=True)
    password = fields.String(dump_only=True)
    cpf_cnpj = fields.String(dump_only=True)
    is_activity = fields.String(dump_only=True)
