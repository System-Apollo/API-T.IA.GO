from flask import Blueprint, jsonify, request
from src.models.company import Company
from src.utils.functions.requests.validators import validar_cpf, validar_cnpj, validar_email
from src.utils.config.extensions import db

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

    required_fields = ['name', 'last_name', 'company_name', 'email', 'password', 'cpf_cnpj']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Converter CPF/CNPJ para string
    cpf_cnpj = str(data['cpf_cnpj'])
    
    # Validação de CPF ou CNPJ
    if not (validar_cpf(cpf_cnpj) or validar_cnpj(cpf_cnpj)):
        return jsonify({"error": "Invalid CPF or CNPJ"}), 400

    # Validação de e-mail
    email = data['email']
    if not validar_email(email):
        return jsonify({"error": "Invalid email format"}), 400

    # Verificar duplicidade de e-mail e CPF/CNPJ
    if User.get_email(email) or User.query.filter_by(cpf_cnpj=cpf_cnpj).first():
        return jsonify({"error": "Email or CPF/CNPJ already exists"}), 409
    
    # Verificar se a empresa já existe; se não, criar uma nova
    company_name = data['company_name']
    company = Company.query.filter_by(name=company_name).first()
    if not company:
        company = Company(name=company_name)
        db.session.add(company)
        db.session.commit()

    new_user = User(
        name=data['name'],
        last_name=data['last_name'],
        company_id=company.id,  # Relacione o usuário à empresa
        email=data['email'],
        password=data['password'],
        cpf_cnpj=data['cpf_cnpj'],
        is_activity=False,
        user_role="Teste"
    )
    new_user.save_to_db()

    return jsonify({"message": "User created", "username": new_user.username}), 201

@auth_bp.post("/login")
def login_user():
    data = request.get_json()
    user = User.get_email(data['email'])



    if user and (user.check_password(data['password'])):
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        if not user.get_activity():
            return jsonify({"error": "Inactivated account"}), 403

        return (
            jsonify(
                {
                    "message": "Login successful",
                    "username": user.username,
                    "role": user.get_role(),
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
