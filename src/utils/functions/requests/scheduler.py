from src.models.company import Company
from src.utils.config.extensions import db

def reset_requests_for_all_companies():
    """Reseta o contador de requisições de todas as empresas."""
    companies = Company.query.all()
    for company in companies:
        company.reset_requests()
    db.session.commit()