from src.utils.config.extensions import db
from datetime import datetime, timezone

class TokenBlocklist(db.Model):
    __tablename__ = 'token_blocklist'
    id = db.Column(db.String, primary_key=True)
    jti = db.Column(db.String, unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return '<TokenBlocklist %r>' % self.jti

    def save(self):
        db.session.add(self)
        db.session.commit()


