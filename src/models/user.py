from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from src.utils.config.extensions import db


def generate_uuid():
    """Gera um UUID único para o ID do usuário."""
    return str(uuid4())


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(512))
    cpf_cnpj = db.Column(db.String(18), unique=True)
    is_activity = db.Column(db.Boolean, default=False)
    user_role = db.Column(db.String(50), default="Teste")

    # Relacionamento com a tabela 'companies'
    company_id = db.Column(db.String, db.ForeignKey('companies.id'), nullable=False)
    company = db.relationship('Company', backref='company_users', lazy=True)

    def __init__(self, name, last_name, company_id, email, password, cpf_cnpj, is_activity=False, user_role="Usuario"):
        """Construtor para inicializar um novo usuário."""
        self.id = generate_uuid()
        self.username = f"{name} {last_name}"
        self.company_id = company_id
        self.email = email
        self.password = generate_password_hash(password)
        self.cpf_cnpj = cpf_cnpj
        self.is_activity = is_activity
        self.user_role = user_role

    def __repr__(self):
        """Representação do objeto como string."""
        return f'<User {self.username}>'

    # Métodos para senha
    def set_password(self, password):
        """Define uma nova senha para o usuário."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verifica se a senha fornecida é válida."""
        return check_password_hash(self.password, password)

    # Métodos para atividade
    def set_activity(self, is_activity):
        """Ativa ou desativa o usuário."""
        self.is_activity = is_activity

    def get_activity(self):
        """Retorna o status de atividade do usuário."""
        return self.is_activity

    # Métodos para nome do usuário
    def get_username(self):
        """Obtém o nome de usuário."""
        return self.username

    def set_username(self, username):
        """Define um novo nome de usuário."""
        self.username = username

    # Métodos para CPF/CNPJ
    def get_cpf_cnpj(self):
        """Obtém o CPF ou CNPJ do usuário."""
        return self.cpf_cnpj

    def set_cpf_cnpj(self, cpf_cnpj):
        """Define um novo CPF ou CNPJ para o usuário."""
        self.cpf_cnpj = cpf_cnpj

    def set_role(self, user_role):
        """Define o papel do usuário."""
        self.user_role = user_role

    def get_role(self):
        """Obtém o papel do usuário."""
        return self.user_role
    

    # Métodos de consulta
    @classmethod
    def get_user_by_username(cls, username):
        """Busca um usuário pelo nome de usuário."""
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_email(cls, email):
        """Busca um usuário pelo email."""
        return cls.query.filter_by(email=email).first()

    # Métodos de banco de dados
    def save_to_db(self):
        """Salva o usuário no banco de dados."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Remove o usuário do banco de dados."""
        db.session.delete(self)
        db.session.commit()

    def update_in_db(self):
        """Atualiza o usuário no banco de dados."""
        db.session.commit()