from flask import Blueprint, jsonify, request

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    current_user,
    get_jwt_identity
)

from src.models.user import User
from src.models.token_blocklist import TokenBlocklist

auth_bp = Blueprint('auth', __name__)


@auth_bp.post("/register")
def register_user():
    data = request.get_json()

    required_fields = ['name', 'last_name', 'company', 'email', 'password', 'cpf_cnpj']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    if User.get_email(data['email']) or User.query.filter_by(cpf_cnpj=data['cpf_cnpj']).first():
        return jsonify({"error": "Email or CPF/CNPJ already exists"}), 409

    new_user = User(
        name=data['name'],
        last_name=data['last_name'],
        company=data['company'],
        email=data['email'],
        password=data['password'],
        cpf_cnpj=data['cpf_cnpj'],
        is_activity=False
    )
    new_user.save_to_db()

    return jsonify({"message": "User created", "username": new_user.username}), 201

@auth_bp.post("/login")
def login_user():
    data = request.get_json()
    user = User.get_email(data['email'])

    if user.get_activity() != True:
        return jsonify({"error": "Inactivated account"}), 403

    if user and (user.check_password(data['password'])):
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return (
            jsonify(
                {
                    "message": "Login successful",
                    "username": user.username,
                    "tokens": {"access_token": access_token, "refresh_token": refresh_token}
                }
            ), 200
        )

    return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.get("/logout")
@jwt_required(verify_type=False)
def logout_user():
    jwt = get_jwt()
    jti = jwt['jti']
    token_type = jwt['type']

    token_b = TokenBlocklist(jti=jti)
    token_b.save_to_db()

    return jsonify({"message": f" {token_type} token revoked successfully"}), 200

@auth_bp.get("/refresh")
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)

    return jsonify({"access_token": new_access_token}), 200


@auth_bp.get("/whoami")
@jwt_required()
def whoami():
    return jsonify(
        {
            "message": "User details",
            "user_details": {
                "username": current_user.username,
                "company": current_user.company,
                "email": current_user.email,
                "cpf_cnpj": current_user.cpf_cnpj
            }
        }
    )
