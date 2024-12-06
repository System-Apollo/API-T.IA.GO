from marshmallow import Schema, fields, post_dump

class UserSchema(Schema):
    id = fields.String(dump_only=True)
    username = fields.String(dump_only=True)
    email = fields.String(dump_only=True)
    cpf_cnpj = fields.String(dump_only=True)
    is_activity = fields.String(dump_only=True)
    user_role = fields.String(dump_only=True)

    # Campos personalizados
    company_name = fields.String(dump_only=True)
    limit_requests = fields.Integer(dump_only=True)
    used_requests = fields.Integer(dump_only=True)

    @post_dump
    def add_company_details(self, data, **kwargs):
        """
        Adiciona detalhes da empresa ao schema serializado.
        """
        if self.context.get('company'):
            company = self.context['company']
            data['company_name'] = company.name
            data['limit_requests'] = company.limit_requests
            data['used_requests'] = company.used_requests
        return data
