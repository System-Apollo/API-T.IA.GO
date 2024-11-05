import queue
from time import sleep, time
from src.utils.functions.conversation.question import processar_pergunta

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


    if agora - ultimo_minuto >= 60:
        requisicoes_no_minuto = 0
        ultimo_minuto = agora


    if agora - ultimo_dia >= 86400:
        requisicoes_no_dia = 0
        ultimo_dia = agora


    if requisicoes_no_minuto >= limite_por_minuto:
        sleep(60 - (agora - ultimo_minuto))
        requisicoes_no_minuto = 0
        ultimo_minuto = time()

    if requisicoes_no_dia >= limite_por_dia:
        raise Exception("Limite diário de requisições atingido.")

    requisicoes_no_minuto += 1
    requisicoes_no_dia += 1



def processar_fila():
    while True:
        pergunta, dataframe = fila_de_requisicoes.get()
        controlar_taxa()
        resposta_texto, grafico_data = processar_pergunta(pergunta, dataframe)
        fila_de_requisicoes.task_done()


def adicionar_pergunta_na_fila(pergunta, dataframe):
    fila_de_requisicoes.put((pergunta, dataframe))
