from flask import Flask, jsonify
from flask_cors import CORS
from threading import Thread
from src.models.token_blocklist import TokenBlocklist
from apscheduler.schedulers.background import BackgroundScheduler
from src.utils.functions.requests.scheduler import reset_requests_for_all_companies  # Importa a função
from src.models.user import User
from src.routes.auth import auth_bp
from src.routes.users import user_bp
from src.routes.tiago import main_bp
from src.routes.upload import upload_bp
from src.utils.config.extensions import db, jwt 
from src.utils.functions.requests.control import processar_fila
from datetime import timedelta

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config.from_prefixed_env()

    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=8)

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()
        
    # Configurar o agendamento do reset mensal
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=reset_requests_for_all_companies, trigger="cron", day=1, hour=0, minute=0)  # Todo dia 1 à meia-noite
    scheduler.start()

    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp, url_prefix='/main')
    app.register_blueprint(upload_bp, url_prefix='/upload')

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_headers, jwt_data):
        identity = jwt_data['sub']
        return User.query.filter_by(id=identity).one_or_none()

    @jwt.additional_claims_loader
    def add_user_claims(identity):
        user = User.query.filter_by(id=identity).one_or_none()

        staff = False
        if user and user.email == 'advprojetos@meirelesefreitas.com.br':
            staff = True

        claims = {"is_staff": staff}

        if user:
            claims["user_id"] = user.id
            claims["company"] = user.company.id if user.company else None  # Use o ID da empresa

        return claims
    @jwt.expired_token_loader
    def expired_token_callback(_jwt_header, jwt_data):
        return jsonify({"message": "Token expired", "error": "token_expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Token is invalid", "error": "token_invalid"}
            ),
            401
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "message": "Token is missing",
                    "error": "auth_token_missing"
                }
            ), 401
        )

    @jwt.token_in_blocklist_loader
    def token_in_blocklist_callback(jwt_header, jwt_data):
        jti = jwt_data['jti']
        token = db.session.query(TokenBlocklist).filter(TokenBlocklist.jti == jti).scalar()

        return token is not None

    thread = Thread(target=processar_fila)
    thread.daemon = True
    thread.start()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
