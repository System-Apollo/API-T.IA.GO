import unicodedata

from src.utils.constants.map import categoria_perguntas
from src.utils.functions.gemini.consult import consultar_gemini_conversacional
from src.utils.functions.processing.processing import *

historico_conversa = []


def carregar_dados(file):
    df = pd.read_excel(file)

    colunas_data = ['Data de distribuição', 'Data de cadastro', 'Data de citação']
    print(colunas_data)
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

def processar_pergunta(pergunta, dataframe):

    pergunta_normalizada = normalizar_pergunta(pergunta)
    greetings = ["olá", "como você está", "oi", "bom dia", "boa tarde", "boa noite", "tudo bem"]
    if any(greeting in pergunta_normalizada.lower() for greeting in greetings):
        resposta_texto = "Como posso te ajudar hoje?"
        historico_conversa.append({"Usuário": pergunta, "TIAGO": resposta_texto})
        return resposta_texto, {}

    for categoria, padroes in categoria_perguntas.items():
        for padrao in padroes:
            if re.search(padrao, pergunta_normalizada, re.IGNORECASE):

                if categoria == 'valor_total_acordos':
                    return processar_valor_acordo(dataframe)
                elif categoria == 'valor_condenacao_estado':
                    return processar_valor_condenacao_por_estado(dataframe)
                elif categoria == 'estado_maior_valor_causa':
                    return processar_maior_valor_causa_por_estado(dataframe)
                elif categoria == 'estado_maior_media_valor_causa':
                    return processar_media_valor_causa_por_estado(dataframe)
                elif categoria == 'divisao_resultados_processos':
                    return processar_sentenca(dataframe, pergunta)
                elif categoria == 'transitaram_julgado':
                    return processar_transito_julgado(dataframe)
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
                elif categoria == 'melhor_estrategia':
                    return consultar_gemini_conversacional(pergunta,
                                                           dataframe), "Essa pergunta envolve uma análise mais detalhada e política de acordo. Por favor, entre em contato com o setor responsável."
                elif categoria == 'beneficio_economico_carteira':
                    return consultar_gemini_conversacional(pergunta,
                                                           dataframe), "Para calcular o benefício econômico, subtraia o valor da condenação do valor da causa."
                elif categoria == 'beneficio_economico_estado':
                    return consultar_gemini_conversacional(pergunta,
                                                           dataframe), "Para calcular o benefício econômico por estado, subtraia o valor da condenação pelo valor da causa em cada estado."
                elif categoria == 'idade_carteira':
                    return consultar_gemini_conversacional(pergunta,
                                                           dataframe), "Para determinar a idade da carteira, consulte os dados de abertura e finalização dos processos."
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
                    return consultar_gemini_conversacional(pergunta,
                                                           dataframe), "Para encontrar o processo mais antigo, verifique a data de distribuição mais antiga no banco de dados."


                historico_conversa.append({"Usuário": pergunta, "TIAGO": "resposta_texto"})
                return "resposta_texto", {}


    chatgemini_resposta = consultar_gemini_conversacional(pergunta, dataframe)
    historico_conversa.append({"Usuário": pergunta, "TIAGO": chatgemini_resposta})
    return chatgemini_resposta, {}
