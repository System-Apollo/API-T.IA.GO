from src.utils.config.extensions import db
from datetime import datetime

class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)  # Nome do arquivo
    filepath = db.Column(db.String(255), nullable=False)  # Caminho do arquivo
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Data de upload

    # Relacionamento com a tabela 'companies'
    company_id = db.Column(db.String, db.ForeignKey('companies.id'), nullable=False)
    company = db.relationship('Company', backref='files')  # Relacionamento

    def __init__(self, filename, company_id, filepath):
        self.filename = filename
        self.company_id = company_id
        self.filepath = filepath

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()