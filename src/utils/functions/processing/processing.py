import pandas as pd
import re
import locale
from datetime import datetime


try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')
import unicodedata

def verificar_colunas(dataframe, colunas_necessarias):
    """
    Verifica se as colunas necessárias estão presentes no DataFrame.
    Retorna True se todas estiverem presentes, ou False e uma lista das colunas ausentes.
    """
    colunas_ausentes = [col for col in colunas_necessarias if col not in dataframe.columns]
    if colunas_ausentes:
        return False, colunas_ausentes
    return True, []

def processar_valor_acordo(dataframe):
    colunas_necessarias = ['Valor de acordo (R$)']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}
    
    if 'Valor de acordo (R$)' in dataframe.columns:


        dataframe['Valor de acordo (R$)'] = dataframe['Valor de acordo (R$)'].astype(str)

        dataframe['Valor de acordo (R$)'] = (
            dataframe['Valor de acordo (R$)']
            .str.replace('R$', '', regex=False)
            .str.replace('.', '', regex=False)
            .str.replace(',', '.', regex=False)
        )

        dataframe['Valor de acordo (R$)'] = pd.to_numeric(dataframe['Valor de acordo (R$)'], errors='coerce')

        valor_total_acordo = dataframe['Valor de acordo (R$)'].sum()

        quantidade_acordos = dataframe[dataframe['Valor de acordo (R$)'] > 0]['Valor de acordo (R$)'].count()

        grafico_data = {
            "Quantidade de Acordos": int(quantidade_acordos),
            "Valor Total": float(valor_total_acordo)
        }

        valor_total_acordo_formatado = f"R$ {valor_total_acordo:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


        return f"O valor total dos acordos é de R$ {valor_total_acordo_formatado} com {quantidade_acordos} acordos.", grafico_data
    else:
        return "Não foi possível calcular o valor total dos acordos, coluna 'Valor do acordo' não encontrada.", {}

def processar_valor_condenacao_por_estado(dataframe):
    colunas_necessarias = ['Valor de causa (R$)','Foro']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}

    dataframe['Valor de condenação (R$)'] = (dataframe['Valor de condenação (R$)']
                                             .astype(str)
                                             .str.replace('R$', '', regex=False)
                                             .str.replace('.', '', regex=False)
                                             .str.replace(',', '.', regex=False))

    dataframe['Valor de condenação (R$)'] = pd.to_numeric(dataframe['Valor de condenação (R$)'], errors='coerce')
    dataframe['Estado'] = dataframe['Foro'].str.extract(r'([A-Z]{2})')

    soma_por_estado = dataframe.groupby('Estado')['Valor de condenação (R$)'].sum()

    resposta_texto = "O valor total de condenações por estado é:\n"
    resposta_texto += "\n".join(
        [f"{estado}: R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') for estado, valor in
         soma_por_estado.items()])

    return resposta_texto, {
        "condenacao_por_estado": soma_por_estado.to_dict()
    }
    
def processar_sentenca(dataframe):
    colunas_necessarias = ['Resultado da Sentença']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}


    sentencas = dataframe['Resultado da Sentença'].str.lower().value_counts().to_dict()

    abreviacoes_sentencas = {
        "sentenca improcedente": "Improcedente",
        "sentenca de extincao sem resolucao do merito": "Sem resolução do mérito",
        "sentenca parcialmente procedente": "Procedente",
        "sentenca de homologacao de acordo": "Acordo"
    }

    sentencas_abreviadas = {abreviacoes_sentencas.get(key, key): value for key, value in sentencas.items()}

    sentencas_texto = ", ".join([f"{sentenca}: {quantidade}" for sentenca, quantidade in sentencas_abreviadas.items()])

    return f"Os resultados das sentenças estão distribuídos da seguinte forma: {sentencas_texto}.", {
        "sentencas": sentencas_abreviadas
    }

def processar_maior_valor_causa_por_estado(dataframe):
    colunas_necessarias = ['Valor de causa (R$)','Foro']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}

    dataframe['Valor de causa (R$)'] = dataframe['Valor de causa (R$)'].astype(str).str.replace('R$', '', regex=False)\
        .str.replace('.', '', regex=False).str.replace(',', '.', regex=False)

    print(dataframe['Valor de causa (R$)'])
    dataframe['Valor de causa (R$)'] = pd.to_numeric(dataframe['Valor de causa (R$)'], errors='coerce')
    print(dataframe['Valor de causa (R$)'])
    dataframe['Estado'] = dataframe['Foro'].str.extract(r'([A-Z]{2})')

    soma_por_estado = dataframe.groupby('Estado')['Valor de causa (R$)'].sum()
    print(soma_por_estado)
    estado_com_maior_valor = soma_por_estado.idxmax()
    maior_valor = soma_por_estado.max()
    print(maior_valor)

    resposta_texto = f"O estado com o maior valor de causa é {estado_com_maior_valor}, com um total de R$ {maior_valor:,.2f}".replace(
        ',', 'X').replace('.', ',').replace('X', '.')

    return resposta_texto, {
        "valor_causa_por_estado": soma_por_estado.to_dict()
    }

def processar_media_valor_causa_por_estado(dataframe):
    colunas_necessarias = ['Valor de causa (R$)','Foro']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}
    
    # Verificar se a coluna "Total da causa" é do tipo string e, se não for, converter para string
    if dataframe['Valor de causa (R$)'].dtype != 'object':
        dataframe['Valor de causa (R$)'] = dataframe['Valor de causa (R$)'].astype(str)

    # Limpar e converter os valores na coluna "Valor de causa (R$)"
    dataframe['Valor de causa (R$)'] = pd.to_numeric(
        dataframe['Valor de causa (R$)']
        .str.replace('R$', '', regex=False)
        .str.replace('.', '', regex=False)
        .str.replace(',', '.', regex=False),
        errors='coerce'
    )

    # Criar uma nova coluna extraindo apenas as siglas dos estados da coluna 'Foro'
    dataframe['Estado'] = dataframe['Foro'].str.extract(r'([A-Z]{2})')

    # Agrupar por estado e calcular a média
    media_valor_por_estado = dataframe.groupby('Estado')['Valor de causa (R$)'].mean().dropna()

    # Encontrar o estado com a maior média
    estado_maior_media = media_valor_por_estado.idxmax()
    maior_media = media_valor_por_estado.max()

    # Formatar a média no estilo brasileiro (R$ X.XXX.XXX,XX)
    resposta_texto = f"O estado com a maior média de valor de causa é {estado_maior_media} com uma média de R$ {maior_media:,.2f}".replace(
        ',', 'X').replace('.', ',').replace('X', '.')

    # Retornar a resposta e os dados do gráfico
    return resposta_texto, {
        "media_valor_causa_por_estado": media_valor_por_estado.to_dict()
    }
# Função auxiliar para processar perguntas sobre "Data de Trânsito em Julgado"
def processar_transito_julgado(dataframe):
    colunas_necessarias = ['Data do trânsito em julgado']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}
    # Verificar quais células da coluna 'Data de Trânsito em Julgado' têm data e quais estão vazias
    transitado = dataframe['Data do trânsito em julgado'].notna() & dataframe['Data do trânsito em julgado'].apply(
        lambda x: str(x).strip() != '-')
    processos_transitados = int(transitado.sum())  # Converte para tipo int nativo
    processos_nao_transitados = int((~transitado).sum())  # Converte para tipo int nativo

    # Retornar a resposta e os dados para o gráfico
    return f"Atualmente, {processos_transitados} processos já transitaram em julgado e {processos_nao_transitados} ainda não.", {
        "transitados": processos_transitados,
        "nao_transitados": processos_nao_transitados
    }
        
def processar_instancia_por_cnj(dataframe, pergunta):
    colunas_necessarias = ['Instância','Resultado da Sentença']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}
    # Preencher valores nulos ou traços na coluna 'Instância' e 'Resultado da Sentença'
    dataframe['Instância'] = dataframe['Instância'].fillna('Sem instância')
    dataframe['Resultado da Sentença'] = dataframe['Resultado da Sentença'].replace('-', 'Sem sentença').fillna('Sem sentença')

    # Mapear valores de "1ª" para "Primeira Instância", etc.
    instancia_map = {
        '1ª': 'Primeira Instância',
        '2ª': 'Segunda Instância',
        '3ª': 'Terceira Instância',
    }
    dataframe['Instância'] = dataframe['Instância'].replace(instancia_map)

    # Manter apenas processos com "Sentença Procedente" ou "Sentença Improcedente"
    dataframe = dataframe[dataframe['Resultado da Sentença'].str.contains("Procedente|Improcedente", case=False, na=False)]

    # Identificar a instância solicitada na pergunta
    if "primeira instancia" in pergunta.lower():
        instancia_solicitada = "Primeira Instância"
    elif "segunda instancia" in pergunta.lower():
        instancia_solicitada = "Segunda Instância"
    elif "terceira instancia" in pergunta.lower():
        instancia_solicitada = "Terceira Instância"
    else:
        return "Não foi possível identificar a instância solicitada na pergunta.", {}

    # Filtrar processos pela instância solicitada
    processos_instancia = dataframe[dataframe['Instância'] == instancia_solicitada]
    total_processos = len(processos_instancia)

    # Se não houver processos na instância solicitada
    if total_processos == 0:
        return f"Não existem processos na {instancia_solicitada}.", {}

    # Contar processos procedentes e improcedentes
    procedentes = processos_instancia[processos_instancia['Resultado da Sentença'].str.contains("Procedente", case=False, na=False)]
    improcedentes = processos_instancia[processos_instancia['Resultado da Sentença'].str.contains("Improcedente", case=False, na=False)]
    total_procedentes = len(procedentes)
    total_improcedentes = len(improcedentes)

    # Resposta textual
    resposta = (
        f"Na {instancia_solicitada}, existem {total_processos} processos no total: "
        f"{total_procedentes} procedentes e {total_improcedentes} improcedentes."
    )

    # Dados para gráficos ou análises adicionais
    grafico_data = {
        "Sentenças Procedentes": total_procedentes,
        "Sentenças Improcedentes": total_improcedentes,
    }

    return resposta, grafico_data
        
def tratar_pergunta_proximas_audiencias(dataframe):
    colunas_necessarias = ['Data de Audiência', 'Vara','Foro', 'Envolvidos - Polo Ativo', 'Tipo de audiência']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}

    dataframe['Data de Audiência'] = pd.to_datetime(dataframe['Data de Audiência'], errors='coerce', format='%d/%m/%Y')

    hoje = datetime.now()
    proximas_audiencias = dataframe[dataframe['Data de Audiência'] >= hoje]

    proximas_audiencias = proximas_audiencias.sort_values(by='Data de Audiência')

    if not proximas_audiencias.empty:
        resposta = "Verificando os dados encontrei:\n"
        for _, row in proximas_audiencias.iterrows():
            resposta += (
                f"\nProcesso {row['Número CNJ']} com audiência em {row['Data de Audiência'].strftime('%d/%m/%Y')}\n"
                f"Local: {row['Vara']}\n"
                f"Foro: {row['Foro']}\n"
                f"Tipo: {row['Tipo de audiência']}\n"
                f"Autor: {row['Envolvidos - Polo Ativo']}.\n\n"
            )
    else:
        resposta = "Você não tem audiências futuras agendadas."

    return resposta,{}        
        
def tratar_pergunta_audiencias_dezembro(dataframe):
    colunas_necessarias = ['Data de Audiência']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)
    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}
    
    dataframe['Data de Audiência'] = pd.to_datetime(dataframe['Data de Audiência'], errors='coerce', format='%d/%m/%Y')
    audiencias_dezembro = dataframe[dataframe['Data de Audiência'].dt.month == 12]
    audiencias_dezembro = audiencias_dezembro.sort_values(by='Data de Audiência')

    if not audiencias_dezembro.empty:
        resposta = f"Encontrei {len(audiencias_dezembro)} audiências agendadas para o mês de dezembro:\n"
        for _, row in audiencias_dezembro.iterrows():
            resposta += (
                f"\nProcesso {row['Número CNJ']} com audiência em {row['Data de Audiência'].strftime('%d/%m/%Y')}\n"
                f"Local: {row['Vara']}\n"
                f"Foro: {row['Foro']}\n"
                f"Tipo: {row['Tipo de audiência']}\n"
                f"Autor: {row['Envolvidos - Polo Ativo']}.\n\n"
            )
    else:
        resposta = "Não há audiências agendadas para o mês de dezembro."

    return resposta.strip(), {}

def processar_quantidade_processos_por_estado(dataframe):
    colunas_necessarias = ['Foro']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}
    # Extrair o estado de cada valor na coluna 'Foro' e criar uma nova coluna 'Estado'
    dataframe['Estado'] = dataframe['Foro'].apply(
        lambda x: re.search(r' - ([A-Z]{2})$', str(x)).group(1) if re.search(r' - ([A-Z]{2})$', str(x)) else None)

    # Filtrar as linhas onde o estado foi extraído corretamente
    dataframe_estados = dataframe.dropna(subset=['Estado'])

    # Agrupar os processos apenas pelo estado e contar a quantidade
    processos_por_estado = dataframe_estados['Estado'].value_counts().to_dict()

    # Preparar a resposta textual
    estados_texto = ", ".join([f"{estado}: {quantidade}" for estado, quantidade in processos_por_estado.items()])
    resposta = f"A quantidade de processos por estado está distribuída da seguinte forma: {estados_texto}."

    # Preparar os dados para o gráfico
    grafico_data = {
        "estados": processos_por_estado
    }

    return resposta, grafico_data

def processar_quantidade_processos_por_comarca(dataframe):
    colunas_necessarias = ['Foro']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}
    # Extrair o município de cada valor na coluna 'Foro', removendo o estado
    dataframe['Municipio'] = dataframe['Foro'].apply(lambda x: str(x).split(' - ')[0] if ' - ' in str(x) else x)

    # Agrupar os processos apenas pelo município e contar a quantidade
    processos_por_municipio = dataframe['Municipio'].value_counts().to_dict()

    # Preparar a resposta textual
    municipios_texto = ", ".join(
        [f"{municipio}: {quantidade}" for municipio, quantidade in processos_por_municipio.items()])
    resposta = f"A quantidade de processos por comarca (município) está distribuída da seguinte forma: {municipios_texto}."

    # Preparar os dados para o gráfico
    grafico_data = {
        "municipios": processos_por_municipio
    }

    return resposta, grafico_data
# Função para contagem de numero de processo ,e separa por ativos e arquivados
def processar_quantidade_processos(dataframe):
    colunas_necessarias = ['Número CNJ']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}
    # Contar a quantidade total de processos
    total_processos = int(dataframe['Número CNJ'].count())

    # Contar os processos ativos e arquivados
    processos_ativos = int(dataframe[dataframe['Status'].str.lower() == 'ativo']['Número CNJ'].count())
    processos_arquivados = int(dataframe[dataframe['Status'].str.lower() == 'arquivado']['Número CNJ'].count())

    # Retornar a resposta e os dados do gráfico
    return f"Há um total de {total_processos} processos. Destes, {processos_ativos} são ativos e {processos_arquivados} estão arquivados.", {
        "ativos": processos_ativos,
        "arquivados": processos_arquivados
    }
# Função para processar o valor total da causa
def processar_valor_total_causa(dataframe):
    colunas_necessarias = ['Valor de causa (R$)', 'Status']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}
    # Converter a coluna 'Total da causa' para string e depois para valores numéricos (removendo símbolos de moeda e ajustando formatação)
    dataframe['Valor de causa (R$)'] = pd.to_numeric(
        dataframe['Valor de causa (R$)']
        .astype(str)  # Converte todos os valores da coluna para string
        .str.replace('R$', '', regex=False)
        .str.replace('.', '', regex=False)
        .str.replace(',', '.', regex=False), errors='coerce'
    )

    # Somar o valor total da causa para todos os processos
    valor_total_causa = dataframe['Valor de causa (R$)'].sum()

    # Dividir o total por status (ativo e arquivado)
    total_ativos = dataframe[dataframe['Status'].str.lower() == 'ativo']['Valor de causa (R$)'].sum()
    total_arquivados = dataframe[dataframe['Status'].str.lower() == 'arquivado']['Valor de causa (R$)'].sum()

    # Formatar os valores no padrão brasileiro
    valor_total_causa_formatado = f"{valor_total_causa:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    total_ativos_formatado = f"{total_ativos:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    total_arquivados_formatado = f"{total_arquivados:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    # Retornar a resposta com o valor total e os dados para o gráfico
    resposta_texto = f"O valor total da causa é de R$ {valor_total_causa_formatado}.\n" \
                     f"Total de ativos: R$ {total_ativos_formatado}.\n" \
                     f"Total de arquivados: R$ {total_arquivados_formatado}."

    # Convertendo para int ou float para JSON serializable
    return resposta_texto, {
        "ativos": float(total_ativos),  # Conversão para tipo nativo
        "arquivados": float(total_arquivados)  # Conversão para tipo nativo
    }
# Função auxiliar para processar perguntas sobre status (ativos, arquivados, etc.)
def processar_status(pergunta, dataframe, status):
    colunas_necessarias = ['Status']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}
    status_lower = status.lower()
    processos_status = dataframe[dataframe['Status'].str.lower() == status_lower]
    quantidade = processos_status.shape[0]

    # Retornar a chave correta dependendo do status
    if status_lower == 'ativo':
        return f"Verifiquei aqui e atualmente, há {quantidade} processos ativos.", {
            "ativos": quantidade,
            "arquivados": dataframe[dataframe['Status'].str.lower() == 'arquivado'].shape[0]
            # Adicionar arquivados para gráfico comparativo
        }
    elif status_lower == 'arquivado':
        return f"Verifiquei aqui e atualmente, há {quantidade} processos arquivados/encerrados.", {
            "ativos": dataframe[dataframe['Status'].str.lower() == 'ativo'].shape[0],
            # Adicionar ativos para gráfico comparativo
            "arquivados": quantidade
        }
    else:
        return f"Verifiquei aqui e atualmente, há {quantidade} processos {status}.", {
            "status": quantidade
        }
# Função para processar a quantidade de recursos interpostos
def processar_quantidade_recursos(dataframe):
    colunas_necessarias = ['Tipos de recursos']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}
    # Remover espaços extras e converter para minúsculas para evitar problemas de formatação
    dataframe['Tipos de recursos'] = dataframe['Tipos de recursos'].str.strip().str.lower()

    # Contar os processos com recursos (diferentes de '-')
    recursos_interpostos = dataframe[dataframe['Tipos de recursos'] != '-'].shape[0]

    # Contar os processos sem recursos
    sem_recursos = dataframe[dataframe['Tipos de recursos'] == '-'].shape[0]

    # Retornar a resposta com a quantidade de recursos interpostos e os dados para o gráfico
    return f"Foram interpostos {recursos_interpostos} recursos, e {sem_recursos} processos não têm recurso.", {
        "com_recursos": recursos_interpostos,
        "sem_recursos": sem_recursos
    }
# Função auxiliar para processar perguntas sobre "Resultado da Sentença"
def processar_sentenca(dataframe, pergunta):
    colunas_necessarias = ['Resultado da Sentença']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}
    sentencas = dataframe['Resultado da Sentença'].str.lower().value_counts().to_dict()

    # Dicionário de abreviações para as sentenças
    abreviacoes_sentencas = {
        "sentenca improcedente": "Improcedente",
        "sentenca de extincao sem resolucao do merito": "Sem resolução do mérito",
        "sentenca parcialmente procedente": "Procedente",
        "sentenca de homologacao de acordo": "Acordo"
    }

    # Substituir as legendas pelas abreviações no dicionário de sentenças
    sentencas_abreviadas = {abreviacoes_sentencas.get(key, key): value for key, value in sentencas.items()}

    # Se a pergunta mencionar "divididos" ou "resultados dos processos", retornamos as divisões das sentenças
    if "divididos" in pergunta.lower() or "resultados dos processos" in pergunta.lower():
        sentencas_texto = ", ".join(
            [f"{sentenca}: {quantidade}" for sentenca, quantidade in sentencas_abreviadas.items()])
        return f"Os resultados das sentenças estão divididos da seguinte forma: {sentencas_texto}.", {
            "sentencas": sentencas_abreviadas
        }

    # Termos comuns relacionados às sentenças
    termos_sentenca = {
        "extinção sem resolução do mérito": "Sem resolução do mérito",
        "parcialmente procedente": "Procedente",
        "improcedente": "Improcedente",
        "homologação de acordo": "Acordo"
    }

    # Verificar se alguma sentença específica foi mencionada na pergunta
    for termo, abreviado in termos_sentenca.items():
        if termo in pergunta.lower():
            quantidade = sentencas_abreviadas.get(abreviado, 0)  # Se não existir, retorna 0
            return f"Atualmente, existem {quantidade} processos com o resultado de {abreviado}.", {
                "sentencas": sentencas_abreviadas  # Sempre retornar todas as sentenças para gráficos
            }

    # Se a sentença específica não for reconhecida
    return "O resultado de sentença especificado não foi encontrado. Os resultados disponíveis são: " + ", ".join(
        sentencas_abreviadas.keys()), {
        "sentencas": sentencas_abreviadas
    }
        
def processar_assuntos_recorrentes(dataframe, incluir_totais=False):
    """
    Processa os assuntos mais recorrentes e retorna os dois principais ou todos com totais.
    
    Args:
        dataframe (DataFrame): Dados contendo a coluna "Assuntos".
        incluir_totais (bool): Se True, inclui o total geral de registros.
        
    Returns:
        str: Texto formatado com os assuntos mais recorrentes.
        dict: Dados com todos os assuntos e suas frequências.
    """
    colunas_necessarias = ['Assuntos']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}

    # Contar a frequência dos assuntos na coluna "Assuntos"
    assuntos = dataframe['Assuntos'].str.lower().value_counts().to_dict()

    if not assuntos:
        return "Não há dados disponíveis para os assuntos.", {}

    # Abreviar os nomes dos assuntos
    assuntos_abreviados = {abreviar_assuntos(assunto): quantidade for assunto, quantidade in assuntos.items()}

    # Preparar resposta para os 2 mais recorrentes
    dois_mais_recorrentes = dict(list(assuntos_abreviados.items())[:2])
    assuntos_texto = ", ".join([f"{assunto}: {quantidade}" for assunto, quantidade in dois_mais_recorrentes.items()])

    # Verificar se a pergunta solicita totais
    if incluir_totais:
        total = sum(assuntos.values())
        return (f"Os dois assuntos mais recorrentes são: {assuntos_texto}. Total de registros: {total}.", 
                {"assuntos": assuntos_abreviados, "total_registros": total})

    return (f"Os dois assuntos mais recorrentes são: {assuntos_texto}.", 
            {"assuntos": assuntos_abreviados})

def processar_tribunal_acoes_convenções(dataframe):
    colunas_necessarias = ['Assuntos','Órgão']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}
    # Filtrar as linhas onde o assunto é "Acordo e Convenção Coletivos de Trabalho"
    convenções = dataframe[
        dataframe['Assuntos'].str.contains('Acordo e Convenção Coletivos de Trabalho', case=False, na=False)]

    # Contar os tribunais (coluna Órgão) associados a essas ações
    tribunais = convenções['Órgão'].value_counts().to_dict()

    # Verificar qual tribunal tem mais ações
    if tribunais:
        tribunal_mais_acoes = max(tribunais, key=tribunais.get)
        quantidade = tribunais[tribunal_mais_acoes]
        return f"O tribunal com mais ações sobre convenções coletivas é {tribunal_mais_acoes} com {quantidade} ações.", {
            "tribunais": tribunais  # Retorna todos os tribunais para o gráfico
        }
    else:
        return "Não foram encontradas ações sobre convenções coletivas nos tribunais.", {}

def processar_rito(dataframe):
    colunas_necessarias = ['Rito']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}
    # Contar a quantidade de processos por tipo de rito
    ritos = dataframe['Rito'].str.lower().value_counts().to_dict()

    # Verificar quantos processos estão no rito sumaríssimo
    quantidade_sumarissimo = ritos.get('sumaríssimo', 0)  # A contagem de "Sumaríssimo" no dataframe

    return f"Há {quantidade_sumarissimo} processos no rito sumaríssimo.", {
        "ritos": ritos  # Retorna todos os ritos para exibição no gráfico
    }

def processar_fase(dataframe, pergunta=None):
    colunas_necessarias = ['Fase']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}
    
    # Converter a coluna 'Fase' para minúsculas para facilitar a comparação
    fases = dataframe['Fase'].str.lower().value_counts().to_dict()

    # Se a pergunta não especifica uma fase particular, retorna todas as fases
    if not pergunta or "fase" in pergunta.lower():
        fases_texto = ", ".join([f"{fase}: {quantidade}" for fase, quantidade in fases.items()])
        return f"As fases estão distribuídas da seguinte forma: {fases_texto}.", {
            "fases": fases
        }

    # Agora, vamos verificar se a pergunta menciona uma fase específica
    termos_fase = {
        "recursal": "recursal",
        "arquivado": "arquivado",
        "finalizado": "finalizado",
        "conciliatória": "conciliatória",
        "julgamento": "julgamento",
        "executória": "executória"
    }

    # Verificar se alguma fase específica foi mencionada na pergunta
    for termo, fase in termos_fase.items():
        if termo in pergunta.lower():
            quantidade = fases.get(fase.lower(), 0)  # Se não existir, retorna 0
            return f"Atualmente, existem {quantidade} processos na fase {fase}.", {
                "fases": fases  # Sempre retornar todas as fases para gráficos
            }

    # Se a fase específica não for reconhecida
    return "A fase especificada não foi encontrada. As fases disponíveis são: " + ", ".join(fases.keys()), {
        "fases": fases
    }

def processar_reclamantes_multiplos(dataframe):
    colunas_necessarias = ['Envolvidos - Polo Ativo']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}
    # Remover qualquer tipo de espaço antes e depois dos nomes
    dataframe['Envolvidos - Polo Ativo'] = dataframe['Envolvidos - Polo Ativo'].str.strip()

    # Contar quantos processos cada reclamante tem
    reclamantes = dataframe['Envolvidos - Polo Ativo'].value_counts()

    # Filtrar os reclamantes que têm mais de um processo
    reclamantes_multiplos = reclamantes[reclamantes > 1].to_dict()

    if len(reclamantes_multiplos) > 0:
        reclamantes_texto = ", ".join(
            [f"{reclamante}: {quantidade} processos" for reclamante, quantidade in reclamantes_multiplos.items()])
        return f"Os reclamantes com mais de um processo são: {reclamantes_texto}.", {
            "reclamantes_multiplos": reclamantes_multiplos  # Dados para gráfico
        }
    else:
        return "Nenhum reclamante tem mais de um processo.", {}

def processar_estado_mais_ofensor(dataframe):
    colunas_necessarias = ['Foro', 'Valor de condenação (R$)']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}
    # Garantir que todos os valores na coluna 'Total deferido' sejam strings antes de aplicar as substituições
    dataframe['Valor de condenação (R$)'] = dataframe['Valor de condenação (R$)'].astype(str).str.replace('R$', '',
                                                                                      regex=False).str.replace('.', '',
                                                                                                               regex=False).str.replace(
        ',', '.', regex=False)

    # Converter para float
    dataframe['Valor de condenação (R$)'] = pd.to_numeric(dataframe['Valor de condenação (R$)'], errors='coerce')

    # Agrupar por estado (Foro) e somar os valores de condenação
    valor_condenacao_por_estado = dataframe.groupby('Foro')['Valor de condenação (R$)'].sum()

    # Verificar qual estado tem o maior valor de condenação
    estado_mais_preocupante = valor_condenacao_por_estado.idxmax()
    maior_valor = valor_condenacao_por_estado.max()

    # Converter os dados para um formato gráfico
    dados_grafico = valor_condenacao_por_estado.to_dict()

    return f"O estado com o maior valor de condenação é {estado_mais_preocupante}, com um total de R$ {maior_valor:,.2f}.", {
        "valor_condenacao_por_estado": dados_grafico  # Dados para o gráfico
    }

def processar_comarca_mais_preocupante(dataframe):
    colunas_necessarias = ['Foro', 'Valor de condenação (R$)']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}
    # Extrair a comarca (município) da coluna 'Foro'
    dataframe['Comarca'] = dataframe['Foro'].apply(extrair_comarca)

    # Verificar se a coluna 'Total deferido' contém valores não-string e converter para string se necessário
    dataframe['Valor de condenação (R$)'] = dataframe['Valor de condenação (R$)'].apply(lambda x: str(x) if pd.notnull(x) else x)

    # Limpar e converter a coluna 'Total deferido' para float, tratando os valores corretamente
    dataframe['Valor de condenação (R$)'] = pd.to_numeric(
        dataframe['Valor de condenação (R$)']
        .str.replace('R$', '', regex=False)
        .str.replace('.', '', regex=False)
        .str.replace(',', '.', regex=False),
        errors='coerce'
    )

    # Agrupar por comarca e somar os valores de condenação
    valor_condenacao_por_comarca = dataframe.groupby('Comarca')['Valor de condenação (R$)'].sum()

    # Verificar qual comarca tem o maior valor de condenação
    comarca_mais_preocupante = valor_condenacao_por_comarca.idxmax()
    maior_valor = valor_condenacao_por_comarca.max()

    # Converter os dados para um formato gráfico
    dados_grafico = valor_condenacao_por_comarca.to_dict()

    # Retornar a resposta e os dados do gráfico
    return f"A comarca com o maior valor de condenação é {comarca_mais_preocupante}, com um total de R$ {maior_valor:,.2f}.", {
        "valor_condenacao_por_comarca": dados_grafico  # Dados para o gráfico
    }

def processar_media_duracao_por_estado(dataframe):
    colunas_necessarias = ['Data do Última mov.', 'Data da distribuição', 'Foro']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}
    # Converter as colunas 'Última mov.' e 'Data de distribuição' para datetime, corrigindo o formato
    dataframe['Data do Última mov.'] = pd.to_datetime(dataframe['Data do Última mov.'], format='%d/%m/%Y', errors='coerce')
    dataframe['Data da distribuição'] = pd.to_datetime(dataframe['Data da distribuição'], format='%d/%m/%Y',
                                                       errors='coerce')

    # Calcular a duração do processo (diferença entre 'Última mov.' e 'Data de distribuição')
    dataframe['Duração'] = (dataframe['Data do Última mov.'] - dataframe['Data da distribuição']).dt.days

    # Remover valores de duração inválidos (NaN)
    dataframe = dataframe.dropna(subset=['Duração'])

    # Verificar se há dados suficientes para continuar
    if dataframe.empty:
        return "Não há dados suficientes para calcular a média de duração por estado.", {}

    # Extrair o estado da coluna 'Foro'
    dataframe['Estado'] = dataframe['Foro'].str.split('-').str[-1].str.strip()

    # Calcular a média de duração por estado
    media_duracao_por_estado = dataframe.groupby('Estado')['Duração'].mean().to_dict()

    if not media_duracao_por_estado:
        return "Não foi possível calcular a média de duração por estado.", {}

    # Identificar o estado com a maior média de duração
    estado_maior_media = max(media_duracao_por_estado, key=media_duracao_por_estado.get)
    maior_media = media_duracao_por_estado[estado_maior_media]

    return f"O estado com a maior média de duração dos processos é {estado_maior_media}, com uma média de {maior_media:.0f} dias.", {
        "media_duracao_por_estado": media_duracao_por_estado
    }

def processar_media_duracao_por_comarca(dataframe):
    colunas_necessarias = ['Data do Última mov.', 'Data da distribuição', 'Foro']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}
    # Converter as colunas 'Última mov.' e 'Data de distribuição' para datetime, corrigindo o formato
    dataframe['Data do Última mov.'] = pd.to_datetime(dataframe['Data do Última mov.'], format='%d/%m/%Y', errors='coerce')
    dataframe['Data da distribuição'] = pd.to_datetime(dataframe['Data da distribuição'], format='%d/%m/%Y',
                                                       errors='coerce')

    # Calcular a duração do processo (diferença entre 'Última mov.' e 'Data de distribuição')
    dataframe['Duração'] = (dataframe['Data do Última mov.'] - dataframe['Data da distribuição']).dt.days

    # Remover valores de duração inválidos (NaN)
    dataframe = dataframe.dropna(subset=['Duração'])

    # Verificar se há dados suficientes para continuar
    if dataframe.empty:
        return "Não há dados suficientes para calcular a média de duração por comarca.", {}

    # Extrair o município (comarca) da coluna 'Foro'
    dataframe['Comarca'] = dataframe['Foro'].str.split('-').str[0].str.strip()

    # Calcular a média de duração por comarca
    media_duracao_por_comarca = dataframe.groupby('Comarca')['Duração'].mean().to_dict()

    if not media_duracao_por_comarca:
        return "Não foi possível calcular a média de duração por comarca.", {}

    # Identificar a comarca com a maior média de duração
    comarca_maior_media = max(media_duracao_por_comarca, key=media_duracao_por_comarca.get)
    maior_media = media_duracao_por_comarca[comarca_maior_media]

    return f"A comarca com a maior média de duração dos processos é {comarca_maior_media}, com uma média de {maior_media:.0f} dias.", {
        "media_duracao_por_comarca": media_duracao_por_comarca
    }

def processar_sentencas_improcedentes(dataframe):
    colunas_necessarias = ['Resultado da Sentença']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}
    # Converter a coluna 'Resultado da Sentença' para minúsculas para garantir consistência
    dataframe['Resultado da Sentença'] = dataframe['Resultado da Sentença'].str.lower()

    # Contar a quantidade de sentenças improcedentes
    quantidade_improcedentes = dataframe[dataframe['Resultado da Sentença'] == 'sentenca improcedente'].shape[0]

    # Contar todos os tipos de sentenças para o gráfico
    sentencas_contagem = dataframe['Resultado da Sentença'].value_counts().to_dict()

    # Abreviações das sentenças para o gráfico
    abreviacoes_sentencas = {
        "sentenca improcedente": "Improcedente",
        "sentenca de extincao sem resolucao do merito": "Sem resolução do mérito",
        "sentenca parcialmente procedente": "Procedente",
        "sentenca de homologacao de acordo": "Acordo"
    }

    # Substituir as legendas pelas abreviações no dicionário de sentenças
    sentencas_abreviadas = {abreviacoes_sentencas.get(key, key): value for key, value in sentencas_contagem.items()}

    # Retornar a resposta e os dados para o gráfico
    return f"Há {quantidade_improcedentes} processos com sentença improcedente.", {
        "sentencas": sentencas_abreviadas
    }

def processar_sentencas_procedentes(dataframe):
    colunas_necessarias = ['Resultado da Sentença']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}
    # Converter a coluna 'Resultado da Sentença' para minúsculas para garantir consistência
    dataframe['Resultado da Sentença'] = dataframe['Resultado da Sentença'].str.lower()

    # Contar a quantidade de sentenças improcedentes
    quantidade_improcedentes = \
    dataframe[dataframe['Resultado da Sentença'] == 'sentenca parcialmente procedente'].shape[0]

    # Contar todos os tipos de sentenças para o gráfico
    sentencas_contagem = dataframe['Resultado da Sentença'].value_counts().to_dict()

    # Abreviações das sentenças para o gráfico
    abreviacoes_sentencas = {
        "sentenca improcedente": "Improcedente",
        "sentenca de extincao sem resolucao do merito": "Sem resolução do mérito",
        "sentenca parcialmente procedente": "Procedente",
        "sentenca de homologacao de acordo": "Acordo"
    }

    # Substituir as legendas pelas abreviações no dicionário de sentenças
    sentencas_abreviadas = {abreviacoes_sentencas.get(key, key): value for key, value in sentencas_contagem.items()}

    # Retornar a resposta e os dados para o gráfico
    return f"Há {quantidade_improcedentes} processos com sentença procedente.", {
        "sentencas": sentencas_abreviadas
    }

def processar_sentencas_extinto_sem_custos(dataframe):
    colunas_necessarias = ['Resultado da Sentença']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}
    # Converter a coluna 'Resultado da Sentença' para minúsculas para garantir consistência
    dataframe['Resultado da Sentença'] = dataframe['Resultado da Sentença'].str.lower()

    # Contar a quantidade de processos extintos sem custos
    extincao_sem_resolucao = \
    dataframe[dataframe['Resultado da Sentença'] == 'sentenca de extincao sem resolucao do merito'].shape[0]
    improcedentes = dataframe[dataframe['Resultado da Sentença'] == 'sentenca improcedente'].shape[0]

    # Soma dos processos sem custos
    total_extinto_sem_custos = extincao_sem_resolucao + improcedentes

    # Contar todos os tipos de sentenças para o gráfico
    sentencas_contagem = dataframe['Resultado da Sentença'].value_counts().to_dict()

    # Abreviações das sentenças para o gráfico
    abreviacoes_sentencas = {
        "sentenca improcedente": "Improcedente",
        "sentenca de extincao sem resolucao do merito": "Sem resolução do mérito",
        "sentenca parcialmente procedente": "Procedente",
        "sentenca de homologacao de acordo": "Acordo"
    }

    # Substituir as legendas pelas abreviações no dicionário de sentenças
    sentencas_abreviadas = {abreviacoes_sentencas.get(key, key): value for key, value in sentencas_contagem.items()}

    # Retornar a resposta e os dados para o gráfico
    return f"Há {total_extinto_sem_custos} processos extintos sem custos (incluindo extinção sem resolução e improcedentes).", {
        "sentencas": sentencas_abreviadas
    }

def processar_maior_tempo_sem_movimentacao(dataframe):
    colunas_necessarias = ['Data da distribuição', 'Data do Última mov.', 'Dias sem movimentação']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}

    dataframe['Data da distribuição'] = pd.to_datetime(dataframe['Data da distribuição'], format='%d/%m/%Y', errors='coerce')
    dataframe['Data do Última mov.'] = pd.to_datetime(dataframe['Data do Última mov.'], format='%d/%m/%Y', errors='coerce')
    dataframe['Dias sem movimentação'] = (dataframe['Data do Última mov.'] - dataframe['Data da distribuição']).dt.days

    processo_maior_tempo = dataframe.loc[dataframe['Dias sem movimentação'].idxmax()]

    numero_processo = processo_maior_tempo['Número CNJ']
    dias_sem_movimentacao = processo_maior_tempo['Dias sem movimentação']

    top_4_processos = dataframe[['Número CNJ', 'Dias sem movimentação']].sort_values(by='Dias sem movimentação', ascending=False).head(4)

    dados_grafico = top_4_processos.set_index('Número CNJ').to_dict()['Dias sem movimentação']

    return f"O processo com maior tempo sem movimentação é o número {numero_processo}, com {dias_sem_movimentacao} dias sem movimentação.", {
        "processos": dados_grafico
    }

def processar_divisao_por_rito(dataframe):
    colunas_necessarias = ['Rito']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}
    # Contar a quantidade de processos por tipo de Rito
    ritos = dataframe['Rito'].str.lower().value_counts().to_dict()

    # Preparar o texto de resposta com os valores de cada rito
    ritos_texto = ", ".join([f"{rito.capitalize()}: {quantidade}" for rito, quantidade in ritos.items()])

    # Preparar os dados para o gráfico
    dados_grafico = {rito.capitalize(): quantidade for rito, quantidade in ritos.items()}

    # Retornar a resposta e os dados para o gráfico
    return f"A divisão dos processos por rito é: {ritos_texto}.", {
        "ritos": dados_grafico
    }

def processar_nao_julgados(dataframe):
    colunas_necessarias = ['Resultado da Sentença']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}
    # Considerar como processos não julgados aqueles sem resultado de sentença
    processos_nao_julgados = dataframe[
        dataframe['Resultado da Sentença'].isnull() | dataframe['Resultado da Sentença'].str.contains('não', case=False,
                                                                                                      na=True)]

    # Quantidade de processos não julgados
    quantidade_nao_julgados = processos_nao_julgados.shape[0]

    # Preparar o texto de resposta
    return f"Atualmente, há {quantidade_nao_julgados} processos que ainda não foram julgados.", {
        "nao_julgados": quantidade_nao_julgados
    }

def processar_nao_citados(dataframe):
    colunas_necessarias = ['Data de citação']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}
    
    # Contar processos que ainda não têm data de citação (processos não citados)
    processos_nao_citados = dataframe[dataframe['Data de citação'].isna()].shape[0]

    # Contar processos que já foram citados
    processos_citados = dataframe[dataframe['Data de citação'].notna()].shape[0]

    # Retornar o texto da resposta e os dados para o gráfico
    return f"Atualmente, há {processos_nao_citados} processos que ainda não foram citados.", {
        "processos_citados": processos_citados,
        "processos_nao_citados": processos_nao_citados
    }

def processar_processo_mais_antigo(dataframe):
    colunas_necessarias = ['Data da distribuição']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}

    # Converter a coluna 'Data da distribuição' para o tipo datetime, ignorando erros de conversão
    dataframe['Data da distribuição'] = pd.to_datetime(dataframe['Data da distribuição'], errors='coerce', format='%d/%m/%Y')

    # Remover linhas com valores de data inválidos (NaT)
    dataframe = dataframe.dropna(subset=['Data da distribuição'])

    # Encontrar a data mínima na coluna 'Data da distribuição'
    data_mais_antiga = dataframe['Data da distribuição'].min()

    # Selecionar o processo correspondente à data mais antiga
    processo_mais_antigo = dataframe[dataframe['Data da distribuição'] == data_mais_antiga]

    # Verificar se o dataframe resultante tem algum valor
    if not processo_mais_antigo.empty:
        # Supondo que a coluna do processo seja chamada 'Número CNJ'
        numero_processo_mais_antigo = processo_mais_antigo['Número CNJ'].values[0]
        data_processo = data_mais_antiga.strftime('%d/%m/%Y')

        # Resposta textual
        resposta = f"O processo mais antigo é o número {numero_processo_mais_antigo}, distribuído em {data_processo}."

        # Dados para gráfico (nesse caso, vazio)
        grafico_data = {}

        return resposta, grafico_data
    else:
        resposta = "Nenhum processo encontrado com uma data válida."
        return resposta, {}

def processar_contagem_classe_cnj(df):
    colunas_necessarias = ['Classe CNJ']
    valido, colunas_ausentes = verificar_colunas(df, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}

    if 'Classe CNJ' not in df.columns:
        raise ValueError("A coluna 'Classe CNJ' não está presente no DataFrame fornecido.")

    total = int(df["Classe CNJ"].count())
    trabalhista_count = int(df['Classe CNJ'].str.contains(r'Ação Trabalhista', case=False, na=False).sum())
    penal_count = int(df['Classe CNJ'].str.contains(r'Ação Penal', case=False, na=False).sum())
    civel_count = int(df['Classe CNJ'].str.contains(r'(Ação Civel|Processo Cível|Cível)', case=False, na=False).sum())
    jec_count = int(df['Classe CNJ'].str.contains(r'(Ação Jec|Processo Juizado especial|JEC)', case=False, na=False).sum())

    resposta = f"""
    O total de processos encontrados é {total}. Aqui está a divisão por classes:
    - Trabalhistas: {trabalhista_count}
    - Penais: {penal_count}
    - Cíveis: {civel_count}
    - Juizado Especial (JEC): {jec_count}
    """

    # Converta para tipos compatíveis com JSON antes de retornar
    return resposta.strip(), {
        "total": total,
        "trabalhista": trabalhista_count,
        "penal": penal_count,
        "civel": civel_count,
        "jec": jec_count
    }

def processar_maior_valor_condenacao(df):
    colunas_necessarias = ['Valor de condenação (R$)','Órgão']
    valido, colunas_ausentes = verificar_colunas(df, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}

    if 'Valor de condenação (R$)' not in df.columns:
        raise ValueError("A coluna 'Valor de condenação (R$)' não está presente no DataFrame fornecido.")

    row_regex = (
        df['Valor de condenação (R$)']
        .str.replace('R$', '', regex=False)
        .str.replace('.', '', regex=False)
        .str.replace(',', '.', regex=False)
    )

    row_number = pd.to_numeric(row_regex, errors='coerce')

    linha_maxima = df.loc[row_number.idxmax()]
    valor_condenacao = linha_maxima['Valor de condenação (R$)']
    numero_cnj = linha_maxima['Número CNJ']
    orgao = linha_maxima['Órgão']

    return f"A sentença mais elevada foi no caso de número {numero_cnj} no valor de {valor_condenacao} em trâmite no {orgao}", {}
# Função auxiliar para processar perguntas sobre órgãos
def processar_orgao(dataframe):
    colunas_necessarias = ['Órgão']
    valido, colunas_ausentes = verificar_colunas(dataframe, colunas_necessarias)

    if not valido:
        return f"Seus dados ainda são para testes. A coluna {', '.join(colunas_ausentes)} não está disponível.", {}

    if 'Órgão' not in dataframe.columns:
        raise ValueError("A coluna 'Órgão' não está presente no DataFrame fornecido.")

    # Contagem de órgãos
    orgaos = dataframe['Órgão'].str.strip().str.lower().value_counts().to_dict()

    # Órgãos mais e menos frequentes
    orgao_mais_frequente = max(orgaos, key=orgaos.get, default=None)
    orgao_menos_frequente = min(orgaos, key=orgaos.get, default=None)

    # Dados estruturados para gráficos
    dados_grafico = {
        "labels": list(orgaos.keys()),
        "values": list(orgaos.values())
    }

    # Resumo textual
    resumo = (
        f"Os órgãos estão distribuídos da seguinte forma:\n"
        f"- Órgão mais frequente: {orgao_mais_frequente.capitalize()} ({orgaos[orgao_mais_frequente]} ocorrências).\n"
        f"- Órgão menos frequente: {orgao_menos_frequente.capitalize()} ({orgaos[orgao_menos_frequente]} ocorrências).\n"
        f"Total de órgãos diferentes: {len(orgaos)}.\n"
    )

    return resumo.strip(), {
        "orgao_mais_frequente": orgao_mais_frequente,
        "orgao_menos_frequente": orgao_menos_frequente,
        "total_orgaos": len(orgaos),
        "distribuicao_orgaos": orgaos,
        "grafico": dados_grafico
    }

def extrair_comarca(foro):
    """Função para extrair o município (comarca) da coluna 'Foro'."""
    match = re.match(r"^(.+?)\s*-\s*[A-Z]{2}", foro)
    if match:
        return match.group(1).strip()  # Retorna o nome do município (comarca)
    return foro  # Caso não encontre o formato esperado, retorna o valor original
# Função auxiliar para abreviar os nomes longos dos assuntos
def abreviar_assuntos(assunto):
    abreviacoes = {
        "acordo e convenção coletivos de trabalho": "Acordo/Convenção",
        "verbas rescisórias": "Verbas Rescisórias",
        "estabilidade acidentária": "Estabilidade Acident.",
        "indenização por dano moral": "Dano Moral",
        "indenização por dano material": "Dano Material",
        "rescisão indireta": "Rescisão Indireta",
        "diferença de comissão": "Dif. Comissão",
        "gestante": "Gestante",
        "doença ocupacional": "Doença Ocup."
        # Adicione mais abreviações conforme necessário
    }

    return abreviacoes.get(assunto.lower(),
                           assunto)  # Retorna a abreviação se houver, caso contrário retorna o original

