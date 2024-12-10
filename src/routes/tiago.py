from flask import Blueprint, request, jsonify
from time import sleep
import os
from src.models.file import File  # Importa o modelo File
from src.models.user import User# Adicionado: Importação do modelo User
from src.models.company import Company
from src.utils.config.extensions import db

from src.utils.functions.conversation.question import carregar_dados, processar_pergunta
from flask_jwt_extended import jwt_required, get_jwt

main_bp = Blueprint('main', __name__)

def obter_base_dados(company):
    """
    Busca o arquivo da base de dados para a empresa no banco de dados.
    """
    # Busca no banco de dados pelo arquivo associado à empresa
    file_record = File.query.filter_by(company_id=company.id).first()
    if file_record and os.path.exists(file_record.filepath):  # Verifica se o arquivo existe fisicamente
        return carregar_dados(file_record.filepath)
    return None

@main_bp.route('/', methods=['GET'])
@jwt_required()
def tela_inicial():
    return jsonify({"mensagem": "Bem-vindo à tela inicial!"}), 200


@main_bp.route('/pergunta', methods=['POST'])
@jwt_required()
def pergunta():
    claims = get_jwt()

    user_id = claims.get('user_id')
    company_id = claims.get('company')
    
    # Verificar se o usuário e a empresa existem
    user = User.query.filter_by(id=user_id).first()
    company = Company.query.filter_by(id=company_id).first()

    if not user:
        return jsonify({"erro": "Usuário não encontrado!"}), 404

    # Verificar se a empresa ainda pode fazer requisições
    if not company.can_make_request():
        return jsonify({
            "resposta": "Limite de requisições mensais da empresa atingido!",
            "grafico": None  # Pode incluir mais detalhes ou deixar `None`
        })

    
    # Carregar a base de dados correspondente
    df = obter_base_dados(company)

    if df is None:
        return jsonify({
            "resposta": "Nenhuma base de dados vinculada ao seu usuário. Solicite suporte!",
            "grafico": None  # Pode incluir mais detalhes ou deixar `None`
        })
    # if df is None:
    #     return jsonify({"erro": "Nenhum arquivo carregado!"}), 400
    
    # Pegar os dados da requisição
    dados = request.get_json()
    pergunta_usuario = dados.get('pergunta', '')

    if not pergunta_usuario:
        return jsonify({"erro": "Pergunta não fornecida!"}), 400

    # Processar a pergunta diretamente e gerar a resposta
    resposta_texto, grafico_data = processar_pergunta(pergunta_usuario, df, user_id)
    
    # Incrementar o número de requisições usadas pela empresa
    try:
        company.increment_requests()
        db.session.commit()
    except Exception as e:
        return jsonify({"erro": f"Erro ao atualizar requisições: {str(e)}"}), 500

    # Retornar a resposta com o texto e os dados do gráfico (se houver)
    return jsonify({
        "resposta": resposta_texto,  # Retorna o texto para o usuário
        "grafico": grafico_data       # Retorna os dados para o gráfico (pode ser None se não houver)
    })

# @main_bp.route('/pergunta', methods=['POST'])
# @jwt_required()
# def pergunta():
#     claims = get_jwt()

#     user_id = claims.get('user_id')
#     company_id = claims.get('company')
    
#     # Verificar se o usuário existe
#     user = User.query.filter_by(id=user_id).first()
#     if not user:
#         return jsonify({"erro": "Usuário não encontrado!"}), 404

#     # Obter a empresa sem verificar sua existência explicitamente
#     company = Company.query.filter_by(id=company_id).first()

#     # Verificar se a empresa ainda pode fazer requisições
#     if company and not company.can_make_request():
#         return jsonify({
#             "resposta": "Limite de requisições mensais da empresa atingido!",
#             "grafico": None
#         })

#     # Carregar a base de dados correspondente
#     df = obter_base_dados(company)
#     if df is None:
#         return jsonify({
#             "resposta": "Nenhuma base de dados vinculada ao seu usuário. Solicite suporte!",
#             "grafico": None
#         })

#     # Pegar os dados da requisição
#     dados = request.get_json()
#     pergunta_usuario = dados.get('pergunta', '')

#     if not pergunta_usuario:
#         return jsonify({"erro": "Pergunta não fornecida!"}), 400

#     # Processar a pergunta diretamente e gerar a resposta
#     resposta_texto, grafico_data = processar_pergunta(pergunta_usuario, df, user_id)
    
#     # Incrementar o número de requisições usadas pela empresa
#     try:
#         if company:
#             company.increment_requests()
#             db.session.commit()
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"erro": f"Erro ao atualizar requisições: {str(e)}"}), 500

#     # Retornar a resposta com o texto e os dados do gráfico (se houver)
#     return jsonify({
#         "resposta": resposta_texto,
#         "grafico": grafico_data
#     })
