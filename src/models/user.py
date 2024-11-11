from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from src.utils.config.extensions import db

def generate_uuid():
    return str(uuid4())

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    name = db.Column(db.String(64), index=True, unique=True)
    last_name = db.Column(db.String(64), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    company = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(512))
    cpf_cnpj = db.Column(db.String(14), unique=True)

    def __init__(self, name, last_name, company, email, password, cpf_cnpj):
        self.id = generate_uuid()
        self.name = name
        self.last_name = last_name
        self.username = f"{name} {last_name}"
        self.company = company
        self.email = email
        self.password = generate_password_hash(password)
        self.cpf_cnpj = cpf_cnpj

    def __repr__(self):
        return f'<User {self.name} {self.last_name}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
