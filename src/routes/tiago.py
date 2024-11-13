from flask import Blueprint, request, jsonify
from time import sleep

from src.utils.functions.conversation.question import carregar_dados, processar_pergunta
from flask_jwt_extended import jwt_required, get_jwt

main_bp = Blueprint('main', __name__)


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

    if company == 'MF Digital Law':
        df = carregar_dados('processos_completos_aleatorios_utf8 (1).xlsx')
        
    elif company == 'Teste':
        df = carregar_dados('dados_user2.xlsx')

    else:
        return jsonify({"resposta": "Nenhuma base de dados vinculada ao seu usuário. Solicite suporte!"})

    # if df is None:
    #     return jsonify({"erro": "Nenhum arquivo carregado!"}), 400

    # Pegar os dados da requisição
    dados = request.get_json()
    pergunta_usuario = dados.get('pergunta', '')

    if not pergunta_usuario:
        return jsonify({"erro": "Pergunta não fornecida!"}), 400

    # Processar a pergunta diretamente e gerar a resposta
    resposta_texto, grafico_data = processar_pergunta(pergunta_usuario, df, user_id)

    # Retornar a resposta com o texto e os dados do gráfico (se houver)
    return jsonify({
        "resposta": resposta_texto,  # Retorna o texto para o usuário
        "grafico": grafico_data       # Retorna os dados para o gráfico (pode ser None se não houver)
    })
