from ratelimit import limits, sleep_and_retry
import os
import google.generativeai as genai
from src.models.user import User

RPM = 15
RPD = 1500

def filtrar_dataframe(pergunta, dataframe):
    palavras_chave = pergunta.split()

    df_filtrado = dataframe[
        dataframe['Envolvidos - Polo Ativo'].str.contains('|'.join(palavras_chave), case=False, na=False)
    ]

    colunas_dataframe = [
        "Número CNJ", "Assuntos", "Classe CNJ", "Foro",
        "Data da distribuição", "Data de cadastro", "Data de citação", "Data da sentença", "Data do acordo",
        "Data do arquivamento", "Data do primeiro acórdão", "Data do trânsito em julgado", "Data do Última mov.",
        "Decisões por instância", "Rito", "Desfecho", "Desfecho do pedido de substituição", "Fase",
        "Indicativo de bloqueio?", "Instância", "Juízes",
        "Envolvidos - Polo Ativo", "Envolvidos - Polo Passivo", "Resultado da Sentença",
        "Possui pedido de substituição", "Segredo de justiça?", "Status", "Tipo de alteração da condenação",
        "Tipos de recursos", "Órgão",
        "TST - Data do trânsito em julgado", "TST - Fase atual", "TST - Órgão judiciante",
        "UF", "Ultimo movimento",
        "Valor de acordo (R$)", "Valor de causa (R$)", "Valor de condenação (R$)", "Valor de custas (R$)",
        "Vara", "Data de Audiência", "Data de Contestação", "Data de recurso",
        "Tipo de audiência", "Data do acórdão", "Data de Sessão de Julgamento", "Data da última audiência realizada",
        "Data da próxima audiência", "Data do último recurso apresentado", "Tipo de Recurso",
    ]

    return df_filtrado[colunas_dataframe] if not df_filtrado.empty else dataframe[colunas_dataframe].head(5)

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

    incluir_contexto_dataframe = any(keyword in pergunta.lower() for keyword in ["dados", "dataframe", "mostrar", "situação", "informações"])

    if incluir_contexto_dataframe:
        dataframe_filtrado = filtrar_dataframe(pergunta, dataframe)
        contexto_dataframe = dataframe_filtrado.to_string(index=False)
    else:
        contexto_dataframe = "Nenhum dado solicitado para esta interação."

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
        return "Desculpe, ainda estou aprimorando minha base de conhecimento. Tente novamente em alguns instantes."