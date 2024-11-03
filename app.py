from flask import Flask, jsonify
from flask_cors import CORS

from src.models.token_blocklist import TokenBlocklist
from src.models.user import User
from src.routes.auth import auth_bp
from src.routes.users import user_bp
from src.routes.tiago import main_bp
from src.utils.config.extensions import db, jwt, cache



def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config.from_prefixed_env()
    cache.init_app(app)

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp, url_prefix='/main')

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_headers, jwt_data):
        identity = jwt_data['sub']
        return User.query.filter_by(username=identity).one_or_none()

    @jwt.additional_claims_loader
    def make_additional_claims(identity):
        if identity == "adminprojetos":
            return {"is_staff": True}

        return {"is_staff": False}

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

    return app
