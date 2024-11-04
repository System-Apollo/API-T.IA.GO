from flask import Blueprint, request, jsonify
from time import sleep
from src.utils.functions.requests.control import adicionar_pergunta_na_fila
from src.utils.config.extensions import cache
from flask_jwt_extended import jwt_required

main_bp = Blueprint('main', __name__)



@main_bp.route('/', methods=['GET'])
@jwt_required()
def tela_inicial():
    return jsonify({"mensagem": "Bem-vindo à tela inicial!"}), 200


@main_bp.route('/pergunta', methods=['POST'])
@jwt_required()
def pergunta():

    global df
    if df is None:
        return jsonify({"erro": "Nenhum arquivo carregado!"}), 400

    dados = request.get_json()
    pergunta_usuario = dados.get('pergunta', '')

    if not pergunta_usuario:
        return jsonify({"erro": "Pergunta não fornecida!"}), 400

    resposta_cache = cache.get(pergunta_usuario)

    if resposta_cache:
        return jsonify(resposta_cache)

    adicionar_pergunta_na_fila(pergunta_usuario, df)

    while not cache.get(pergunta_usuario):
        sleep(1)


    resposta_cache = cache.get(pergunta_usuario)
    return jsonify(resposta_cache)
