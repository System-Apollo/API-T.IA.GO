from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from src.database.schema import UserSchema
from src.models.user import User
from src.models.company import Company
from src.utils.functions.requests.scheduler import reset_requests_for_all_companies
from src.utils.config.extensions import db


user_bp = Blueprint('user', __name__)

@user_bp.get("/all")
@jwt_required()
def get_all_users():
    claims = get_jwt()

    if claims.get("is_staff"):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        users_paginated = User.query.paginate(page=page, per_page=per_page)
        
        users_with_context = []
        for user in users_paginated.items:
            company = user.company  # Acessa a empresa relacionada
            schema = UserSchema(context={'company': company})  # Adiciona o contexto
            users_with_context.append(schema.dump(user))

        return (
            jsonify(
                {
                    'users': users_with_context
                }
            )
        )

    return jsonify({"message": "You are not logged in!"}), 403


@user_bp.put("/update/<string:email>")
@jwt_required()
def update_user(email):
    claims = get_jwt()  # Obter informações do token JWT
    data = request.get_json()

    # Verificar se o usuário atual tem permissão para realizar alterações
    if not claims.get("is_staff"):
        return jsonify({"message": "Unauthorized to perform this action!"}), 403

    # Obter o usuário a ser atualizado
    user = User.get_email(email)

    if not user:
        return jsonify({"message": "User not found"}), 404

    try:
        # Atualizar informações gerais do usuário
        if "name" in data and "last_name" in data:
            user.set_username(f"{data['name']} {data['last_name']}")

        # Atualizar atividade
        if "is_activity" in data:
            # Converta o valor para booleano explicitamente
            is_active = data["is_activity"] in [True, "true", "True", 1, "1"]
            user.set_activity(is_active)

        if "cpf_cnpj" in data:
            user.set_cpf_cnpj(data['cpf_cnpj'])

        if "user_role" in data:
            user.set_role(data['user_role'])
            print(f"Atualizando user_role para: {user.get_role()}")# Atualiza diretamente

        # Atualizar informações da empresa associada
        if "company_name" in data:
            company = user.company  # Relacionamento definido no modelo
            if not company:
                return jsonify({"message": "Company not found"}), 404
            company.set_company_name(data["company_name"])

        if "limit_requests" in data:
            company = user.company
            if not company:
                return jsonify({"message": "Company not found"}), 404
            company.set_limit_requests(int(data["limit_requests"]))
        

        # Salvar alterações no banco
        db.session.commit()

        return jsonify({"message": "User successfully updated!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error: {str(e)}"}), 400
    
@user_bp.delete("/delete/<string:email>")
@jwt_required()
def delete_user(email):
    claims = get_jwt()

    # Verificar se o usuário tem permissão para deletar
    if not claims.get("is_staff"):
        return jsonify({"message": "Unauthorized to delete users!"}), 403

    # Buscar o usuário pelo e-mail
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "User not found!"}), 404

    try:
        # Excluir o usuário do banco de dados
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"User with email {email} successfully deleted!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred while deleting the user: {str(e)}"}), 500
    
    
@user_bp.post("/reset-requests")
@jwt_required()
def reset_requests():
    claims = get_jwt()

    if not claims.get("is_staff"):
        return jsonify({"message": "Only staff can reset requests"}), 403

    try:
        reset_requests_for_all_companies()
        return jsonify({"message": "Requests reset successfully!"}), 200
    except Exception as e:
        return jsonify({"error": f"Error resetting requests: {str(e)}"}), 500