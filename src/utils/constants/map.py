from collections import defaultdict

# Dicionário para mapear tipos de perguntas e suas variacoes
categoria_perguntas = defaultdict(list)

# Mapeamento de categorias para funcoes com 8 variacoes de perguntas para cada
categoria_perguntas['valor_total_acordos'] = [ #error
    r"valor total de acordos",
    r"qual o valor total dos acordos",
    r"quanto foi o total de acordos",
    r"total de acordos",
    r"acordos no total",
    r"quantos acordos foram feitos",
    r"qual foi o valor acordado no total",
    r"total acordado"
]

categoria_perguntas['valor_condenacao_estado'] = [ #mudar estado
    r"valor de condenacao por estado",
    r"quanto foi condenado por estado",
    r"qual o valor da condenacao em cada estado",
    r"condenacao total por estado",
    r"condenacao por cada estado",
    r"condenacao de estados",
    r"qual foi a condenacao nos estados",
    r"condenacoes por estado"
]

categoria_perguntas['estado_maior_valor_causa'] = [ #error
    r"estado com maior valor da causa",
    r"qual estado tem o maior valor da causa",
    r"qual estado tem a maior causa",
    r"estado com a maior causa",
    r"estado que tem a causa mais alta",
    r"maior causa por estado",
    r"qual estado teve a maior causa",
    r"estado com causa mais alta"
]

categoria_perguntas['prox_audiencia'] = [ #error
    r"quais sao minhas próximas audiências",
    r"próximas audiências",
    r"quando sao as próximas audiências",
    r"tenho alguma audiência marcada",
    r"minhas audiências futuras",
    r"quando é minha próxima audiência",
    r"qual é a próxima audiência",
    r"me informe sobre minhas próximas audiências"
]

categoria_perguntas['estado_maior_media_valor_causa'] = [
    r"estado com maior media de valor da causa",
    r"qual estado tem a maior media da causa",
    r"qual estado tem a maior média de causa",
    r"qual a maior média de causa por estado",
    r"estado com a maior média de valor de causa",
    r"maior média de valor de causa por estado",
    r"qual estado teve a maior média de causas",
    r"média mais alta de causas por estado"
]

categoria_perguntas['divisao_resultados_processos'] = [ #error
    r"divisao dos resultados dos processos",
    r"como estao divididos os resultados",
    r"divisao dos processos por resultado",
    r"resultados dos processos divididos",
    r"divisao de processos",
    r"resultados de processos",
    r"como estao os resultados dos processos",
    r"dividir resultados dos processos"
]

categoria_perguntas['transitaram_julgado'] = [  #error ?????
    r"processos que transitaram em julgado",
    r"quais processos transitaram em julgado",
    r"transitaram em julgado",
    r"quais processos já transitaram em julgado",
    r"já transitaram em julgado",
    r"processos transitados em julgado",
    r"quantos processos transitaram em julgado",
    r"número de processos transitados"
]

categoria_perguntas['quantidade_processos_estado'] = [
    r"quantidade de processos por estado",
    r"quantos processos existem em cada estado",
    r"número de processos por estado",
    r"quantos processos por estado",
    r"processos por estado",
    r"processos em cada estado",
    r"quantos processos há por estado",
    r"processos divididos por estado"
]

categoria_perguntas['quantidade_processos_comarca'] = [
    r"quantidade de processos por comarca",
    r"quantos processos existem em cada comarca",
    r"número de processos por comarca",
    r"quantos processos por comarca",
    r"processos por comarca",
    r"processos em cada comarca",
    r"quantos processos há por comarca",
    r"processos divididos por comarca"
]

categoria_perguntas['quantidade_total_processos'] = [
    r"quantidade total de processos",
    r"quantos processos existem no total",
    r"quantos processos ao todo",
    r"total de processos",
    r"quantos processos existem",
    r"número total de processos",
    r"processos no total",
    r"total de casos"
]

categoria_perguntas['valor_total_causa'] = [ #?
    r"valor total da causa",
    r"qual o valor total das causas",
    r"total de valor de causa",
    r"quanto foi o valor total das causas",
    r"qual o valor de todas as causas",
    r"valor total das causas",
    r"quanto foi o total das causas",
    r"valor global das causas"
]

categoria_perguntas['processos_ativos'] = [
    r"quantos processos ativos",
    r"processos ativos",
    r"quantos processos tenho ativos",
    r"número de processos ativos",
    r"processos que estao ativos",
    r"quais processos estao ativos",
    r"número de casos ativos",
    r"quais sao os processos ativos"
]

categoria_perguntas['processos_arquivados'] = [
    r"quantos processos arquivados",
    r"processos arquivados",
    r"número de processos arquivados",
    r"quais processos foram arquivados",
    r"arquivamento de processos",
    r"processos já arquivados",
    r"processos que já foram arquivados",
    r"quantos casos arquivados"
]

categoria_perguntas['quantidade_recursos'] = [ #??
    r"quantos recursos foram interpostos",
    r"número de recursos interpostos",
    r"recursos interpostos",
    r"quantos recursos foram feitos",
    r"quantos recursos existem",
    r"número total de recursos",
    r"recursos feitos",
    r"quantos recursos já foram interpostos"
]

categoria_perguntas['sentencas'] = [ ## ?
    r"divisao dos resultados das sentencas",
    r"divisao das sentencas",
    r"como estao divididos os resultados das sentencas",
    r"divisao das decisoes",
    r"sentencas divididas",
    r"quais foram as sentencas",
    r"resultados das sentencas",
    r"sentencas proferidas"
]

categoria_perguntas['assuntos_recorrentes'] = [
    r"assuntos mais recorrentes",
    r"quais os assuntos mais recorrentes",
    r"assuntos mais frequentes",
    r"quais os assuntos mais frequentes",
    r"temas mais recorrentes",
    r"temas mais frequentes",
    r"assuntos mais comuns",
    r"quais sao os assuntos mais comuns"
]

categoria_perguntas['tribunal_acoes_convencoes'] = [
    r"tribunal tem mais acoes sobre convencoes coletivas",
    r"qual tribunal tem mais casos sobre convencoes coletivas",
    r"quais tribunais têm mais acoes de convencoes coletivas",
    r"tribunal com mais casos sobre convencoes coletivas",
    r"quais tribunais têm mais convencoes coletivas",
    r"qual tribunal lida com mais convencoes coletivas",
    r"tribunal que tem mais casos de convencoes coletivas",
    r"quais tribunais têm mais acoes relacionadas a convencoes coletivas"
]

categoria_perguntas['rito_sumarisimo'] = [
    r"rito sumarisimo",
    r"processos no rito sumarissimo",
    r"quantos processos estao no rito sumarissimo",
    r"casos no rito sumarissimo",
    r"quais processos seguem o rito sumarissimo",
    r"quais casos estao no rito sumarissimo",
    r"número de processos no rito sumarissimo",
    r"processos sumarissimos"
]

categoria_perguntas['divisao_fase'] = [ #???
    r"divisao por fase",
    r"como está a divisao dos processos por fase",
    r"processos divididos por fase",
    r"qual é a divisao dos processos por fase",
    r"como estao os processos divididos por fase",
    r"fases dos processos",
    r"divisao dos processos por fase",
    r"quais sao as fases dos processos"
]

categoria_perguntas['reclamantes_multiplos'] = [
    r"algum reclamante tem mais de um processo",
    r"reclamantes com mais de um processo",
    r"tem algum reclamante com múltiplos processos",
    r"reclamantes que possuem mais de um processo",
    r"quem tem mais de um processo",
    r"quais reclamantes têm mais de um processo",
    r"reclamantes com múltiplos processos",
    r"reclamante com mais de um processo"
]

categoria_perguntas['estado_mais_ofensor'] = [
    r"estado devo ter mais preocupacao",
    r"estado mais ofensor",
    r"qual estado é o mais preocupante",
    r"em qual estado devo me preocupar mais",
    r"estado que mais ofende",
    r"estado mais preocupante",
    r"qual estado tem maior risco",
    r"estado com maior risco"
]

categoria_perguntas['comarca_mais_ofensora'] = [ ## error
    r"comarca devo ter mais preocupacao",
    r"comarca mais ofensora",
    r"qual comarca é a mais preocupante",
    r"comarca com maior risco",
    r"comarca mais arriscada",
    r"comarca com mais ofensas",
    r"qual comarca tem mais riscos",
    r"em qual comarca devo me preocupar mais"
]

categoria_perguntas['maior_media_duracao_estado'] = [
    r"estado com maior media de duracao",
    r"qual estado tem a maior media de duracao",
    r"qual estado tem maior duracao média",
    r"estado com maior duracao média",
    r"qual estado leva mais tempo para finalizar os processos",
    r"qual estado tem a maior média de tempo de processos",
    r"estado que leva mais tempo em processos",
    r"estado com a maior média de tempo em processos"
]

categoria_perguntas['maior_media_duracao_comarca'] = [
    r"comarca com maior media de duracao",
    r"qual comarca tem a maior media de duracao",
    r"qual comarca tem maior duracao média",
    r"comarca com maior duracao média",
    r"qual comarca leva mais tempo para finalizar os processos",
    r"qual comarca tem a maior média de tempo de processos",
    r"comarca que leva mais tempo em processos",
    r"comarca com a maior média de tempo em processos"
]

categoria_perguntas['processos_improcedentes'] = [
    r"quantos processos improcedentes",
    r"quantos processos improcedente",
    r"processos julgados improcedentes",
    r"quais os processos foram improcedentes",
    r"quais os processos foram improcedente",
    r"processos improcedentes",
    r"casos julgados improcedentes",
    r"número de processos improcedentes"
]

categoria_perguntas['processos_procedentes'] = [
    r"quantos processos procedentes",
    r"processos julgados procedentes",
    r"quais os processos foram procedentes",
    r"quais os processos foram procedente",
    r"processos procedentes",
    r"casos julgados procedentes",
    r"número de processos procedentes",
    r"quais casos foram procedentes"
]

categoria_perguntas['processos_extintos_sem_custos'] = [
    r"quantos processos extintos sem custos",
    r"processos extintos sem custos",
    r"processos sem custos extintos",
    r"quantos processos foram extintos sem custos",
    r"número de processos extintos sem custos",
    r"processos extintos sem custos totais",
    r"quais processos foram extintos sem custos",
    r"extincao de processos sem custos"
]

categoria_perguntas['processo_maior_tempo_sem_movimentacao'] = [ ##error
    r"processo com maior tempo sem movimentacao",
    r"qual processo está mais tempo sem movimentacao",
    r"processo que está mais tempo parado",
    r"qual processo nao tem movimentacao há mais tempo",
    r"qual o processo mais parado",
    r"processo sem movimentacao há mais tempo",
    r"processo com maior tempo parado",
    r"qual o processo com maior inatividade"
]

categoria_perguntas['divisao_por_rito'] = [
    r"como está a divisao por rito", ## quem respondeu foi o gemini
    r"qual a divisao dos processos por rito",
    r"como é a divisao por rito dos processos",
    r"processos divididos por rito",
    r"qual é a divisao dos processos por rito",
    r"quais sao os ritos dos processos",
    r"processos por rito",
    r"como estao os processos divididos por rito"
]

categoria_perguntas['processos_nao_julgados'] = [ #erro
    r"quantos processos ainda nao foram julgados",
    r"processos nao julgados",
    r"quais processos ainda nao foram julgados",
    r"número de processos nao julgados",
    r"quais casos ainda nao foram julgados",
    r"processos pendentes de julgamento",
    r"processos que ainda nao foram julgados",
    r"quantos casos nao foram julgados"
]

categoria_perguntas['processos_nao_citados'] = [ #erro
    r"quantos processos ainda nao foram citados",
    r"processos nao citados",
    r"quais processos ainda nao foram citados",
    r"número de processos nao citados",
    r"quais casos ainda nao foram citados",
    r"processos pendentes de citacao",
    r"processos que ainda nao foram citados",
    r"quantos casos nao foram citados"
]

categoria_perguntas['processo_mais_antigo'] = [
    r"processo mais antigo da base",
    r"qual o processo mais antigo",
    r"qual é o processo mais antigo",
    r"processo mais antigo",
    r"qual caso é o mais antigo",
    r"caso mais antigo",
    r"número do processo mais antigo",
    r"quais sao os processos mais antigos"
]
