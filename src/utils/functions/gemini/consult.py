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
                                  'Data do Última mov.']  # Ajuste conforme necessário
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
def consultar_gemini_conversacional(pergunta, dataframe, user_id):

    from src.utils.functions.conversation.question import historico_conversa

    configurar_gemini()
    model = genai.GenerativeModel("gemini-1.5-pro-001")


    dataframe_filtrado = filtrar_dataframe(pergunta, dataframe)

    if dataframe_filtrado is None:
        return "Desculpe, não encontrei dados relevantes com base na sua pergunta."

    contexto = dataframe_filtrado.to_string(index=False)


    historico_usuario = historico_conversa.get(user_id, [])

    if historico_usuario:
        contexto_conversa = "\n".join([f"{msg['pergunta']}: {msg['resposta_tiago']}" for msg in historico_usuario[-5:]])
    else:
        contexto_conversa = "Nenhum histórico de conversa disponível."

    prompt = (f"Contexto da conversa:\n{contexto_conversa}\n"
              f"Os dados a seguir são extraídos de um arquivo Excel:\n{contexto}\n\n"
              f"Converse com o usuário e responda de maneira amigável e educada, sem muito lhe questionar: {pergunta}")

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Erro ao consultar a API do Gemini: {e}")
        return "Desculpe, ainda estou aprimorando minha base de conhecimento. Tente novamente em alguns instantes."
