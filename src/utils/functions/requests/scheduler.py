from src.models.user import User
from src.utils.config.extensions import db

def reset_requests_for_all_users():
    """
    Reseta o contador de requisições usadas de todos os usuários.
    """
    users = User.query.all()
    for user in users:
        user.reset_requests()
    db.session.commit()
