from ratelimit import limits, sleep_and_retry
import os
import google.generativeai as genai


# Limites da API do ChatGemini
RPM = 10  # 2 requisições por minuto
RPD = 800  # 50 requisições por dia


def contar_tokens(texto):
    return len(texto.split())


def filtrar_dataframe(pergunta, dataframe):
    # Extrair o nome do autor da pergunta, por exemplo, "Tassio"
    palavras_chave = pergunta.split()
    # Tentar filtrar pela coluna "Envolvidos - Polo Ativo" para encontrar o nome do autor
    if 'Envolvidos - Polo Ativo' in dataframe.columns:
        # Filtrar DataFrame com base na coluna "Envolvidos - Polo Ativo"
        df_filtrado = dataframe[
            dataframe['Envolvidos - Polo Ativo'].str.contains('|'.join(palavras_chave), case=False, na=False)]

        # Se houver dados filtrados, reduzir o número de colunas para as mais relevantes
        if not df_filtrado.empty:
            colunas_relevantes = ['Número CNJ', 'Data da distribuição', 'Status',
                                  'Última mov.']  # Ajuste conforme necessário
            df_filtrado = df_filtrado[colunas_relevantes]
        else:
            return None  # Se não encontrar, retorna None
    else:
        return None  # Se não houver a coluna "Envolvidos - Polo Ativo"
    return df_filtrado


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
    from src.utils.functions.conversation.question import historico_conversa
    model = genai.GenerativeModel("gemini-1.5-pro-001")

    dataframe_filtrado = filtrar_dataframe(pergunta, dataframe)
    contexto = dataframe_filtrado.to_string(index=False)
    contexto_conversa = "\n".join([f"{msg['Usuário']}: {msg['TIAGO']}" for msg in historico_conversa[-5:]])
    prompt = (f"Contexto da conversa:\n{contexto_conversa}"
              f"Os dados a seguir são extraídos de um arquivo Excel:\n{contexto}\n\nConverse com o usuário e responda de maneira amigável e educada, sem muito lhe questionar: {pergunta}")

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
