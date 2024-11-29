from flask import Blueprint, request, jsonify
from time import sleep
import os
from src.models.file import File  # Importa o modelo File
from src.models.user import User  # Adicionado: Importação do modelo User

from src.utils.functions.conversation.question import carregar_dados, processar_pergunta
from flask_jwt_extended import jwt_required, get_jwt

main_bp = Blueprint('main', __name__)

def obter_base_dados(company):
    """
    Busca o arquivo da base de dados para a empresa no banco de dados.
    """
    # Busca no banco de dados pelo arquivo associado à empresa
    file_record = File.query.filter_by(company=company).first()
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
    company = claims.get('company')
    
    # Buscar o usuário no banco de dados
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"erro": "Usuário não encontrado!"}), 404

    # Verificar se o usuário ainda pode fazer requisições
    if not user.can_make_request():
        return jsonify({"erro": "Limite de requisições mensais atingido!"}), 403

    
    # Carregar a base de dados correspondente
    df = obter_base_dados(company)

    if df is None:
        return jsonify({"resposta": "Nenhuma base de dados vinculada ao seu usuário. Solicite suporte!"}), 400
    # if df is None:
    #     return jsonify({"erro": "Nenhum arquivo carregado!"}), 400
    
    # Pegar os dados da requisição
    dados = request.get_json()
    pergunta_usuario = dados.get('pergunta', '')

    if not pergunta_usuario:
        return jsonify({"erro": "Pergunta não fornecida!"}), 400

    # Processar a pergunta diretamente e gerar a resposta
    resposta_texto, grafico_data = processar_pergunta(pergunta_usuario, df, user_id)
    
    # Incrementar o número de requisições usadas pelo usuário
    try:
        user.increment_requests()
        user.update_in_db()
    except Exception as e:
        return jsonify({"erro": f"Erro ao atualizar requisições: {str(e)}"}), 500

    # Retornar a resposta com o texto e os dados do gráfico (se houver)
    return jsonify({
        "resposta": resposta_texto,  # Retorna o texto para o usuário
        "grafico": grafico_data       # Retorna os dados para o gráfico (pode ser None se não houver)
    })

