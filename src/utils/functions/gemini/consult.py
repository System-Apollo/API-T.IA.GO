from ratelimit import limits, sleep_and_retry
import os
import google.generativeai as genai
from src.models.user import User

RPM = 15
RPD = 1500

def filtrar_dataframe(pergunta, dataframe):
    # Mapeamento de palavras-chave para colunas
    mapa_colunas = {
        "envolvido": ["Advogados polo ativo", "Advogados polo passivo"],
        "cnj": ["Número CNJ"],
        "assunto": ["Assuntos"],
        "classe": ["Classe CNJ"],
        "foro": ["Foro"],
        "data": [
            "Data da distribuição", "Data de cadastro", "Data de recurso",
            "Data do acórdão", "Data de Sessão de Julgamento", "Data da última audiência realizada",
            "Data da próxima audiência", "Data do último recurso apresentado"
        ],
        "valor": ["Valor de acordo (R$)", "Valor de causa (R$)", "Valor de condenação (R$)", "Valor de custas (R$)"],
        "resultado": ["Resultado da Sentença"],
        "status": ["Status"],
        "rito": ["Rito"],
        "instância": ["Instância"],
        "teses": ["Teses de Defesa"]
    }

    # Identificar colunas relevantes com base na pergunta
    colunas_relevantes = set()
    for palavra, colunas in mapa_colunas.items():
        if palavra in pergunta.lower():
            colunas_relevantes.update(colunas)

    # Garantir colunas padrão caso nenhuma palavra-chave seja detectada
    if not colunas_relevantes:
        colunas_relevantes = {"Número CNJ", "Classe CNJ","Vara" 
                              "Status", "Envolvidos - Polo Ativo", 
                              "Órgão", 'Foro', 'Data da sentença',
                              'Data do arquivamento', 'UF',
                              'Valor de condenação (R$)', 'Valor de causa (R$)',
                              'Data de Audiência', 'Data do Última mov.',
                              'Desfecho', 'Instância', 'Juízes'}

    # Verificar quais colunas existem no DataFrame
    colunas_existentes = [col for col in colunas_relevantes if col in dataframe.columns]

    # Caso nenhuma coluna seja detectada ou encontrada, envie a base completa
    if not colunas_existentes:
        return (
            f"A pergunta não identificou colunas específicas na base ou elas não estão disponíveis. A base completa será enviada para análise.",
            dataframe
        )

    # Filtrar colunas existentes
    dataframe_filtrado = dataframe[colunas_existentes]

    # Filtrar linhas com base nas palavras-chave presentes na pergunta
    palavras_chave = pergunta.split()
    dataframe_filtrado = dataframe_filtrado[
        dataframe_filtrado.apply(lambda row: any(str(value).lower() in pergunta.lower() for value in row), axis=1)
    ]

    return dataframe_filtrado

def configurar_gemini():
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

@sleep_and_retry
@limits(calls=RPM, period=60)
@limits(calls=RPD, period=86400)
def consultar_gemini_conversacional(pergunta, dataframe, user_id):
    from src.utils.functions.conversation.question import historico_conversa

    configurar_gemini()

    model = genai.GenerativeModel("gemini-1.5-pro-002")

    user = User.query.filter_by(id=user_id).first()

    historico_usuario = historico_conversa.get(user_id, [])
    contexto_conversa = (
        "\n".join([f"{msg['pergunta']}: {msg['resposta_tiago']}" for msg in historico_usuario[-3:]])
        if historico_usuario
        else "Nenhum histórico de conversa disponível."
    )

    

    
    dataframe_filtrado = filtrar_dataframe(pergunta, dataframe)
    if isinstance(dataframe_filtrado, tuple):  # Caso seja necessário enviar a base completa
        mensagem, dataframe_filtrado = dataframe_filtrado
        print(mensagem)  # Log para informar que a base completa está sendo enviada

    
    contexto_dataframe = dataframe_filtrado.to_string(index=False)


    prompt = (f"Usuário que você está conversando (seja gentil com ele(a)): {user.username}\n\n"
              f"Use saudações com esse usuário quando for requisitado. "
              f"Contexto da última interação (use apenas como referência se for relevante): {contexto_conversa}\n\n"
              f"Dados disponíveis: {contexto_dataframe}\n\n"
              f"Responda apenas à pergunta atual, sem repetir respostas ou saudações anteriores. "
              f"Se for solicitado por informações específicas, forneça diretamente, sem introduções ou repetições.\n\n"
              f"Pergunta do usuário: {pergunta}")

    print("Prompt enviado para o modelo:\n", prompt)

    total_tokens = model.count_tokens(prompt)
    print("Número total de tokens na entrada:", total_tokens)

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Erro ao consultar a API do Gemini: {e}")
        return "Desculpe, Não consegui localizar esse dados. Tente novamente em alguns instantes."