from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
import os
from src.utils.config.config import UPLOAD_FOLDER
from src.models.file import File  # Importa o modelo File
from src.models.company import Company
from src.utils.config.extensions import db

upload_bp = Blueprint('upload', __name__)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Cria a pasta de uploads, se necessário

@upload_bp.route('/add', methods=['POST'])
@jwt_required()
def upload_base():
    claims = get_jwt()

    # Verifica se o usuário tem permissão de administrador
    if not claims.get("is_staff"):
        return jsonify({"message": "Unauthorized"}), 403

    # Obtém o arquivo e a empresa da requisição
    file = request.files.get('file')
    company_name = request.form.get('company')
    confirm = request.form.get('confirm', 'false').lower()

    if not file or not company_name:
        return jsonify({"message": "File and company name are required"}), 400

    # Verifica se a empresa existe no banco
    company = Company.query.filter_by(name=company_name).first()
    if not company:
        return jsonify({"message": f"Company {company_name} not found"}), 404

    # Verifica se já existe um arquivo para a empresa
    existing_file = File.query.filter_by(company_id=company.id).first()
    if existing_file and confirm != 'true':  # Arquivo existente e substituição não confirmada
        return jsonify({
            "message": f"A base para a empresa {company_name} já existe.",
            "existing_file": existing_file.filename,
            "action_required": "Pass 'confirm=true' to overwrite the existing file."
        }), 200

    # Salva o arquivo no diretório de uploads
    filename = f"{company_name}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # Salva os metadados do arquivo no banco de dados
    if existing_file:  # Atualiza o registro existente
        existing_file.filename = filename
        existing_file.filepath = file_path
        db.session.commit()
    else:  # Cria um novo registro
        new_file = File(filename=filename, company_id=company.id, filepath=file_path)
        new_file.save_to_db()

    return jsonify({
        "message": "File uploaded and base added.",
        "company": company_name,
        "file_path": file_path
    }), 200
