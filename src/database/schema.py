from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(dump_only=True)
    last_name = fields.String(dump_only=True)
    username = fields.String(dump_only=True)
    company = fields.String(dump_only=True)
    email = fields.String(dump_only=True)
    cpf_cnpj = fields.String(dump_only=True)
    is_activity = fields.String(dump_only=True)
    user_role = fields.String(dump_only=True)
    request_limit = fields.String(dump_only=True)
    requests_used = fields.String(dump_only=True)
