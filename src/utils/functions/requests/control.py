import queue
from time import sleep, time
from src.utils.functions.conversation.question import processar_pergunta
from src.utils.config.extensions import cache

fila_de_requisicoes = queue.Queue()
limite_por_minuto = 4
limite_por_dia = 100
requisicoes_no_minuto = 0
requisicoes_no_dia = 0
ultimo_minuto = time()
ultimo_dia = time()


def controlar_taxa():
    global requisicoes_no_minuto, requisicoes_no_dia, ultimo_minuto, ultimo_dia

    agora = time()

    # Resetar contador por minuto se necessário
    if agora - ultimo_minuto >= 60:
        requisicoes_no_minuto = 0
        ultimo_minuto = agora

    # Resetar contador por dia se necessário
    if agora - ultimo_dia >= 86400:
        requisicoes_no_dia = 0
        ultimo_dia = agora

    # Verificar se está dentro do limite
    if requisicoes_no_minuto >= limite_por_minuto:
        sleep(60 - (agora - ultimo_minuto))  # Aguardar até o próximo minuto
        requisicoes_no_minuto = 0
        ultimo_minuto = time()

    if requisicoes_no_dia >= limite_por_dia:
        raise Exception("Limite diário de requisições atingido.")  # Opcional: Retornar erro ou gerenciar de outra forma

    requisicoes_no_minuto += 1
    requisicoes_no_dia += 1


# Função para processar fila de requisições
def processar_fila():
    while True:
        pergunta, dataframe = fila_de_requisicoes.get()
        controlar_taxa()  # Controlar a taxa antes de processar a requisição
        resposta_texto, grafico_data = processar_pergunta(pergunta, dataframe)
        fila_de_requisicoes.task_done()  # Marcar como finalizada
        cache.set(pergunta, {"resposta": resposta_texto, "grafico": grafico_data})  # Armazenar no cache


def adicionar_pergunta_na_fila(pergunta, dataframe):
    fila_de_requisicoes.put((pergunta, dataframe))
