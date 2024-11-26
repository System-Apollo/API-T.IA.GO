from src.utils.config.extensions import db
from datetime import datetime

class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)  # Nome do arquivo
    company = db.Column(db.String(64), nullable=False)    # Empresa associada
    filepath = db.Column(db.String(255), nullable=False)  # Caminho do arquivo
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Data de upload

    def __init__(self, filename, company, filepath):
        self.filename = filename
        self.company = company
        self.filepath = filepath

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
