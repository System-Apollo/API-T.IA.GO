from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt

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
    claims = get_jwt()
    data = request.get_json()

    if not (claims.get("is_staff")):
        return jsonify({"message": "You are not logged in!"}), 403

    user = User.get_email(email)

    try:
        user.set_username(f"{data['name']} {data['last_name']}")
        user.set_activity(data['activity'])
        user.set_company(data['company'])
        user.set_cpf_cnpj(data['cpf_cnpj'])

        user.update_in_db()

        return jsonify({"message": "You have successfully updated!"}), 200
    except Exception as e:
        return jsonify({"message": f"error: {str(e)}"}), 403
