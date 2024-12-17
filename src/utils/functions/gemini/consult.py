# from ratelimit import limits, sleep_and_retry
# import os
# import google.generativeai as genai
# from src.models.user import User

# RPM = 15
# RPD = 1500

def filtrar_dataframe(pergunta, dataframe):
    # Colunas padrão a serem retornadas
    colunas_padrao = [
        "Número CNJ", "Classe CNJ", "Vara", "Status", "Envolvidos - Polo Ativo",
        "Órgão", "Foro", "Data da sentença", "Data do arquivamento", "UF",
        "Valor de condenação (R$)", "Valor de causa (R$)", "Data de Audiência",
        "Data do Última mov.", "Desfecho", "Instância", "Juízes"
    ]
    
    # Verificar quais colunas padrão existem no DataFrame
    colunas_existentes = [col for col in colunas_padrao if col in dataframe.columns]

    # Caso nenhuma coluna padrão seja encontrada, retorna a base completa
    if not colunas_existentes:
        return (
            "Nenhuma das colunas padrão foi encontrada na base. A base completa será enviada para análise.",
            dataframe
        )
    
    # Filtrar DataFrame apenas com as colunas existentes
    dataframe_filtrado = dataframe[colunas_existentes]

    return dataframe_filtrado

# def configurar_gemini():
#     genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# @sleep_and_retry
# @limits(calls=RPM, period=60)
# @limits(calls=RPD, period=86400)
# def consultar_gemini_conversacional(pergunta, dataframe, user_id):
#     from src.utils.functions.conversation.question import historico_conversa

#     configurar_gemini()

#     model = genai.GenerativeModel("gemini-1.5-pro-002")

#     user = User.query.filter_by(id=user_id).first()

#     historico_usuario = historico_conversa.get(user_id, [])
#     contexto_conversa = (
#         "\n".join([f"{msg['pergunta']}: {msg['resposta_tiago']}" for msg in historico_usuario[-3:]])
#         if historico_usuario
#         else "Nenhum histórico de conversa disponível."
#     )

    

    
#     dataframe_filtrado = filtrar_dataframe(pergunta, dataframe)
#     if isinstance(dataframe_filtrado, tuple):  # Caso seja necessário enviar a base completa
#         mensagem, dataframe_filtrado = dataframe_filtrado
#         print(mensagem)  # Log para informar que a base completa está sendo enviada

    
#     contexto_dataframe = dataframe_filtrado.to_string(index=False)


#     prompt = (f"Usuário que você está conversando (seja gentil com ele(a)): {user.username}\n\n"
#               f"Use saudações com esse usuário quando for requisitado. "
#               f"Contexto da última interação (use apenas como referência se for relevante): {contexto_conversa}\n\n"
#               f"Dados disponíveis: {contexto_dataframe}\n\n"
#               f"Responda apenas à pergunta atual, sem repetir respostas ou saudações anteriores. "
#               f"Se for solicitado por informações específicas, forneça diretamente, sem introduções ou repetições.\n\n"
#               f"Pergunta do usuário: {pergunta}")

#     print("Prompt enviado para o modelo:\n", prompt)

#     total_tokens = model.count_tokens(prompt)
#     print("Número total de tokens na entrada:", total_tokens)

#     try:
#         response = model.generate_content(prompt)
#         return response.text.strip()
#     except Exception as e:
#         print(f"Erro ao consultar a API do Gemini: {e}")
#         return "Desculpe, Estamos passando por uma manunteção em nossa IA aguarde alguns instantes para retorna."

import os
import vertexai
from vertexai.generative_models import GenerativeModel
from ratelimit import limits, sleep_and_retry
from src.models.user import User

# Configurações de limite
RPM = 15
RPD = 1500

def configurar_vertex_ai():
    # Verificar se a variável de ambiente está configurada
    credenciais = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credenciais or not os.path.exists(credenciais):
        raise EnvironmentError(
            f"Arquivo de credenciais não encontrado: {credenciais}. Verifique a configuração da variável GOOGLE_APPLICATION_CREDENTIALS."
        )
    # Inicializa o Vertex AI
    vertexai.init(
        project=os.environ["VERTEX_AI_PROJECT_ID"], 
        location=os.environ["VERTEX_AI_LOCATION"]  # Exemplo: "southamerica-east1"
    )

@sleep_and_retry
@limits(calls=RPM, period=60)
@limits(calls=RPD, period=86400)
def consultar_gemini_conversacional(pergunta, dataframe, user_id):
    from src.utils.functions.conversation.question import historico_conversa

    # Configuração do Vertex AI
    configurar_vertex_ai()

    # Instancia o modelo generativo
    model = GenerativeModel("gemini-1.5-pro-002")

    # Obter histórico do usuário
    user = User.query.filter_by(id=user_id).first()
    historico_usuario = historico_conversa.get(user_id, [])
    contexto_conversa = (
        "\n".join([f"{msg['pergunta']}: {msg['resposta_tiago']}" for msg in historico_usuario[-3:]])
        if historico_usuario
        else "Nenhum histórico de conversa disponível."
    )

    # Filtrar DataFrame com base na pergunta
    dataframe_filtrado = filtrar_dataframe(pergunta, dataframe)
    if isinstance(dataframe_filtrado, tuple):  # Base completa caso nenhuma coluna específica seja encontrada
        mensagem, dataframe_filtrado = dataframe_filtrado
        print(mensagem)

    # Transformar DataFrame em string
    contexto_dataframe = dataframe_filtrado.to_string(index=False)

    # Construção do prompt
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

    # Configurações de geração
    generation_config = {
        "temperature": 0.7,  # Controle de criatividade
        "max_output_tokens": 1024  # Máximo de tokens na resposta
    }

    try:
        # Gera a resposta usando o modelo
        responses = model.generate_content(
            [prompt],
            generation_config=generation_config,
            stream=False,  # Use streaming apenas se quiser processar a resposta em partes
        )

        # Extrai o texto da resposta
        if responses and hasattr(responses, 'text'):
            return responses.text.strip()
        else:
            return "Nenhuma resposta foi gerada."
    except Exception as e:
        print(f"Erro ao consultar a API do Vertex AI: {e}")
        return "Desculpe, estamos passando por uma manutenção em nossa IA. Por favor, tente novamente mais tarde."
    
# import requests
# import json   
# def consultar_tiago_ia(pergunta, dataframe, user_id):
#     from src.utils.functions.conversation.question import historico_conversa
#     """
#     Conecta à IA personalizada via endpoint do Ngrok para responder à pergunta fornecida.

#     :param pergunta: Pergunta do usuário.
#     :param contexto: Contexto adicional ou histórico (opcional).
#     :param user_id: ID do usuário para referência (opcional).
#     :return: Resposta da IA.
#     """
#      # Obter histórico do usuário
#     user = User.query.filter_by(id=user_id).first()
#     historico_usuario = historico_conversa.get(user_id, [])
#     contexto_conversa = (
#         "\n".join([f"{msg['pergunta']}: {msg['resposta_tiago']}" for msg in historico_usuario[-3:]])
#         if historico_usuario
#         else "Nenhum histórico de conversa disponível."
#     )
#     # Filtrar DataFrame com base na pergunta
#     dataframe_filtrado = filtrar_dataframe(pergunta, dataframe)
#     if isinstance(dataframe_filtrado, tuple):  # Base completa caso nenhuma coluna específica seja encontrada
#         mensagem, dataframe_filtrado = dataframe_filtrado
#         print(mensagem)

#     # Transformar DataFrame em string
#     contexto_dataframe = dataframe_filtrado.to_string(index=False)
#     url = "https://b370-187-32-212-210.ngrok-free.app/api/generate"

#     prompt = (f"Usuário que você está conversando (seja gentil com ele(a)): {user.username}\n\n"
#               f"Use saudações com esse usuário quando for requisitado. "
#               f"Contexto da última interação (use apenas como referência se for relevante): {contexto_conversa}\n\n"
#               f"Dados disponíveis: {contexto_dataframe}\n\n"
#               f"Responda apenas à pergunta atual, sem repetir respostas ou saudações anteriores. "
#               f"Se for solicitado por informações específicas, forneça diretamente, sem introduções ou repetições.\n\n"
#               f"Pergunta do usuário: {pergunta}")

#     payload = {
#         "model": "tiago-assistant:alpha",
#         "prompt": prompt
#     }
#     print(payload)

#     try:
#         response = requests.post(url, json=payload)

#         # Verifica o status da resposta
#         if response.status_code != 200:
#             return f"Erro ao consultar a IA: {response.status_code} - {response.text}"

#         # Verifica o tipo de conteúdo retornado
#         if response.headers.get('Content-Type') == 'application/json':
#             return response.json().get("response", "Nenhuma resposta foi gerada.")
#         else:
#             # Processa resposta no formato streaming de linhas
#             lines = response.text.strip().split('\n')
#             responses = [json.loads(line).get("response", "") for line in lines if line.strip()]
#             return ''.join(responses) if responses else "Nenhuma resposta válida foi gerada."

#     except requests.exceptions.RequestException as e:
#         return print(f'Erro IA tiago {e}')