import unicodedata
from src.utils.constants.map import categoria_perguntas
from src.utils.functions.gemini.consult import consultar_gemini_conversacional
from src.utils.functions.processing.processing import *

#Histórico de Conversa transformado em um Objeto
historico_conversa = {}

def carregar_dados(file):
    df = pd.read_excel(file)

    colunas_data = [
        'Data da distribuição',
        'Data da sentença',
        'Data do acordo',
        'Data Apólice',
        'Data do arquivamento',
        'Data do primeiro acórdão',
        'Data do trânsito em julgado',
        'Data do Última mov.',
        'TST - Data do primeiro acórdão',
        'TST - Data do trânsito em julgado',
        'Data de Audiência',
        'Data de Contestação',
        'Data de Contestação',
        'Data de recurso',
        'Data do acórdão',
        'Data de Sessão de Julgamento',
        'Data da última audiência realizada',
        'Data da próxima audiência',
        'Data do último recurso apresentado',
    ]


    for coluna in colunas_data:
        if coluna in df.columns:
            df[coluna] = pd.to_datetime(df[coluna], format='%d/%m/%Y', errors='coerce')

    return df

def normalizar_pergunta(pergunta):

    pergunta = ''.join(
        c for c in unicodedata.normalize('NFD', pergunta) if unicodedata.category(c) != 'Mn'
    )

    pergunta = re.sub(r'[^\w\s]', '', pergunta)
    return pergunta.lower().strip()

def remover_acentos(texto):
    return ''.join(c for c in unicodedata.normalize('NFKD', texto) if not unicodedata.combining(c))


def processar_pergunta(pergunta, dataframe, user_id):
    print(f"Pergunta recebida: {pergunta}")
    pergunta_normalizada = normalizar_pergunta(pergunta)
    print(f"Pergunta normalizada: {pergunta_normalizada}")
    grafico_data = None
    if user_id not in historico_conversa:
        historico_conversa[user_id] = []

    for categoria, padroes in categoria_perguntas.items():
        for padrao in padroes:
            if re.search(padrao, pergunta_normalizada, re.IGNORECASE):
                resultado, grafico_data = processar_categoria(categoria, dataframe, pergunta)

                # Adicionar a pergunta e a resposta no histórico
                historico_conversa[user_id].append({"pergunta": pergunta, "resposta_tiago": resultado})

                # Retornar o texto da resposta e os dados do gráfico (se houver)
                return resultado, grafico_data

    # Caso não encontre uma categoria, utilizar a API de conversação
    chatgemini_resposta = consultar_gemini_conversacional(pergunta, dataframe, user_id)

    # Adicionar ao histórico
    historico_conversa[user_id].append({"pergunta": pergunta, "resposta_tiago": chatgemini_resposta})

    return chatgemini_resposta, grafico_data

def processar_categoria(categoria, dataframe, pergunta):
    if categoria == 'valor_total_acordos':
        return processar_valor_acordo(dataframe)
    elif categoria == 'valor_condenacao_estado':
        return processar_valor_condenacao_por_estado(dataframe)
    elif categoria == 'divisao_resultados_processos':
        return processar_sentenca(dataframe)
    elif categoria == 'estado_maior_valor_causa':
        return processar_maior_valor_causa_por_estado(dataframe)
    elif categoria == 'estado_maior_media_valor_causa':
        return processar_media_valor_causa_por_estado(dataframe)
    elif categoria == 'transitaram_julgado':
        return processar_transito_julgado(dataframe)
    elif categoria == "instancia_":
        return processar_instancia_por_cnj(dataframe)
    elif categoria == 'prox_audiencia':
        return tratar_pergunta_proximas_audiencias(dataframe)
    elif categoria == 'audiencia_dezembro':
        return tratar_pergunta_audiencias_dezembro(dataframe)
    elif categoria == 'quantidade_processos_estado':
        return processar_quantidade_processos_por_estado(dataframe)
    elif categoria == 'quantidade_processos_comarca':
        return processar_quantidade_processos_por_comarca(dataframe)
    elif categoria == 'quantidade_total_processos':
        return processar_quantidade_processos(dataframe)
    elif categoria == 'valor_total_causa':
        return processar_valor_total_causa(dataframe)
    elif categoria == 'processos_ativos':
        return processar_status(pergunta, dataframe, "ativo")
    elif categoria == 'processos_arquivados':
        return processar_status(pergunta, dataframe, "arquivado")
    elif categoria == 'quantidade_recursos':
        return processar_quantidade_recursos(dataframe)
    elif categoria == 'sentencas':
        return processar_sentenca(dataframe, pergunta)
    elif categoria == 'assuntos_recorrentes':
        return processar_assuntos_recorrentes(dataframe)
    elif categoria == 'tribunal_acoes_convencoes':
        return processar_tribunal_acoes_convenções(dataframe)
    elif categoria == 'rito_sumarisimo':
        return processar_rito(dataframe)
    elif categoria == 'divisao_fase':
        return processar_fase(dataframe)
    elif categoria == 'reclamantes_multiplos':
        return processar_reclamantes_multiplos(dataframe)
    elif categoria == 'estado_mais_ofensor':
        return processar_estado_mais_ofensor(dataframe)
    elif categoria == 'comarca_mais_ofensora':
        return processar_comarca_mais_preocupante(dataframe)
    elif categoria == 'maior_media_duracao_estado':
        return processar_media_duracao_por_estado(dataframe)
    elif categoria == 'maior_media_duracao_comarca':
        return processar_media_duracao_por_comarca(dataframe)
    elif categoria == 'processos_improcedentes':
        return processar_sentencas_improcedentes(dataframe)
    elif categoria == 'processos_procedentes':
        return processar_sentencas_procedentes(dataframe)
    elif categoria == 'processos_extintos_sem_custos':
        return processar_sentencas_extinto_sem_custos(dataframe)
    elif categoria == 'processo_maior_tempo_sem_movimentacao':
        return processar_maior_tempo_sem_movimentacao(dataframe)
    elif categoria == 'divisao_por_rito':
        return processar_divisao_por_rito(dataframe)
    elif categoria == 'processos_nao_julgados':
        return processar_nao_julgados(dataframe)
    elif categoria == 'processos_nao_citados':
        return processar_nao_citados(dataframe)
    elif categoria == 'processo_mais_antigo':
        return processar_processo_mais_antigo(dataframe)
    elif categoria == 'classe_cnj':
        return processar_contagem_classe_cnj(dataframe)
    elif categoria == 'valor_sentenca':
        return processar_maior_valor_condenacao(dataframe)
