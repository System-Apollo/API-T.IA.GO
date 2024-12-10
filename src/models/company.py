from uuid import uuid4
from src.utils.config.extensions import db

def generate_uuid():
    """Gera um UUID único para o ID da empresa."""
    return str(uuid4())

class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    name = db.Column(db.String(64), unique=True, nullable=False)
    limit_requests = db.Column(db.Integer, default=50)  # Limite mensal de requisições
    used_requests = db.Column(db.Integer, default=0)    # Requisições usadas no mês

    def can_make_request(self):
        """Verifica se a empresa ainda pode fazer requisições."""
        return self.used_requests < self.limit_requests

    def increment_requests(self):
        """Incrementa o número de requisições usadas pela empresa."""
        self.used_requests += 1

    def reset_requests(self):
        """Reseta o contador de requisições usadas para zero."""
        self.used_requests = 0
        
    def set_company_name(self, new_name):
        """Atualiza o nome da empresa."""
        self.name = new_name

    def set_limit_requests(self, new_limit):
        """Atualiza o limite de requisições da empresa."""
        self.limit_requests = new_limit

    def update_in_db(self):
        """Confirma as alterações no banco de dados."""
        db.session.commit()