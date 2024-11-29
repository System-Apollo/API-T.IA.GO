from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from src.utils.functions.requests.scheduler import reset_requests_for_all_users
from src.database.schema import UserSchema
from src.models.user import User

user_bp = Blueprint('user', __name__)

@user_bp.get("/all")
@jwt_required()
def get_all_users():
    claims = get_jwt()

    if claims.get("is_staff"):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        users = User.query.paginate(page=page, per_page=per_page)
        result = UserSchema(many=True).dump(users)

        return (
            jsonify(
                {
                    'users': result
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

        if "activity" in data:
            user.set_activity(data['activity'])

        if "company" in data:
            user.set_company(data['company'])

        if "cpf_cnpj" in data:
            user.set_cpf_cnpj(data['cpf_cnpj'])

        # Atualizar o papel do usuário (role), somente permitido pelo e-mail autorizado
        if "role" in data:
            if data["role"] == "Admin" and claims.get("is_staff"):
                user.set_role("Admin")  # Permitir atualização para Admin
            elif data["role"] != "Admin":
                user.set_role(data["role"])  # Permitir qualquer outro papel
            else:
                return jsonify({"message": "Only staff can assign Admin role!"}), 403

        user.update_in_db()

        return jsonify({"message": "User successfully updated!"}), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 400
    

@user_bp.post("/reset-requests")
@jwt_required()
def reset_requests():
    claims = get_jwt()

    if not claims.get("is_staff"):
        return jsonify({"message": "Only staff can reset requests"}), 403

    try:
        reset_requests_for_all_users()
        return jsonify({"message": "Requests reset successfully!"}), 200
    except Exception as e:
        return jsonify({"error": f"Error resetting requests: {str(e)}"}), 500