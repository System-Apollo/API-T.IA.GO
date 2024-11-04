from flask import Blueprint, request, jsonify
from time import sleep

from src.utils.functions.conversation.question import carregar_dados, processar_pergunta
from src.utils.functions.requests.control import adicionar_pergunta_na_fila
from flask_jwt_extended import jwt_required

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET'])
@jwt_required()
def tela_inicial():
    return jsonify({"mensagem": "Bem-vindo à tela inicial!"}), 200


@main_bp.route('/pergunta', methods=['POST'])
@jwt_required()
def pergunta():

    # Carregar os dados
    df = carregar_dados('dados_falsos_processos_completos.xlsx')

    if df is None:
        return jsonify({"erro": "Nenhum arquivo carregado!"}), 400

    # Pegar os dados da requisição
    dados = request.get_json()
    print(dados)
    pergunta_usuario = dados.get('pergunta', '')

    if not pergunta_usuario:
        return jsonify({"erro": "Pergunta não fornecida!"}), 400

    # Processar a pergunta diretamente e gerar a resposta
    resposta_texto, grafico_data = processar_pergunta(pergunta_usuario, df)

    # Retornar a resposta diretamente para o usuário
    return jsonify({
        "resposta": resposta_texto,
        "grafico": grafico_data
    })
