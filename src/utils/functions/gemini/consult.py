from ratelimit import limits, sleep_and_retry
import os
from src.utils.functions.conversation.question import historico_conversa
import google.generativeai as genai


# Limites da API do ChatGemini
RPM = 10  # 2 requisições por minuto
RPD = 800  # 50 requisições por dia


def contar_tokens(texto):
    return len(texto.split())

def extrair_palavras_chave(pergunta):
    # Exemplo de lista de palavras-chave que podem estar relacionadas às perguntas
    palavras_chave = ["valor", "estado", "condenação", "processo", "comarca", "rito", "benefício", "economia", "idade"]

    # Verificar se as palavras-chave aparecem na pergunta
    return [palavra for palavra in palavras_chave if palavra in pergunta.lower()]


def filtrar_dataframe_por_palavras_chave(dataframe, palavras_chave):
    filtro = dataframe.apply(lambda row: any(palavra in row.to_string().lower() for palavra in palavras_chave), axis=1)
    return dataframe[filtro]


# Configurar a API do Gemini
def configurar_gemini():
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])  # Certifique-se de ter a chave de API do Gemini no seu .env


# Função modificada para consultar a API do Gemini sem mencionar o nome da planilha
@sleep_and_retry
@limits(calls=RPM, period=60)
@limits(calls=RPD, period=86400)
def consultar_gemini_conversacional(pergunta, dataframe):
    # Configurar a API do Gemini para conversas genéricas
    configurar_gemini()  # Certifique-se de ter a chave de API do Gemini no seu .env
    model = genai.GenerativeModel("gemini-1.5-pro-001")

    palavras_chave = extrair_palavras_chave(pergunta)
    df_filtrado = filtrar_dataframe_por_palavras_chave(dataframe, palavras_chave)
    contexto = df_filtrado.to_string(index=False)
    contexto_conversa = "\n".join([f"{msg['Usuário']}: {msg['TIAGO']}" for msg in historico_conversa[-5:]])
    prompt = (f"Contexto da conversa:\n{contexto_conversa}"
              f"Os dados a seguir são extraídos de um arquivo Excel:\n{contexto}\n\nConverse com o usuário e responda de maneira amigável e educada, nao me traga emojis: {pergunta}")

    tokens_enviados = contar_tokens(prompt)
    print(f"Tokens enviados: {tokens_enviados}")

    try:
        # Enviar a pergunta para o Gemini e obter uma resposta
        response = model.generate_content(prompt)
        tokens_recebidos = contar_tokens(response.text)
        print(f"Tokens recebidos: {tokens_recebidos}")
        return response.text.strip()  # Retorna a resposta como string limpa
    except Exception as e:
        print(f"Erro ao consultar a API do Gemini: {e}")
        return "Desculpe, ainda estou aprimorando minha base de conhecimento. Tente novamente em alguns instantes."
