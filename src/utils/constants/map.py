from collections import defaultdict

categoria_perguntas = defaultdict(list)


categoria_perguntas['audiencia_dezembro'] =[
    r"Quantas audiencias teremos no mes de dezembro",
    r"total de audiencias para o mes de dezembro",
    r"quantas audiencias teremos em dezembro",
]
    
categoria_perguntas['instancia_'] = [
    r"Algum deles foi julgado em primeira instancia",
    r"Algum deles foi julgado em segunda instancia",
    r"Algum deles foi julgado em terceira instancia",
    r"Qual o processo julgado em terceira instancia",
    r"Qual o processo julgado em segunda instancia",
    r"Qual o processo julgado em primeira instancia",
    r"instancia"
]
categoria_perguntas['valor_total_acordos'] = [
    r"valor total de acordos",
    r"qual o valor total dos acordos",
    r"quanto foi o total de acordos",
    r"total de acordos",
    r"acordos no total",
    r"quantos acordos foram feitos",
    r"qual foi o valor acordado no total",
    r"total acordado"
]

categoria_perguntas['valor_condenacao_estado'] = [
    r"valor de condenacao por estado",
    r"quanto foi condenado por estado",
    r"qual o valor da condenacao em cada estado",
    r"condenacao total por estado",
    r"condenacao por cada estado",
    r"condenacao de estados",
    r"qual foi a condenacao nos estados",
    r"condenacoes por estado"
]

categoria_perguntas['estado_maior_valor_causa'] = [
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
    r"quais sao minhas proximas audiencias",
    r"proximas audiencias",
    r"quando sao as proximas audiencias",
    r"tenho alguma audiencia marcada",
    r"minhas audiencias futuras",
    r"quando e minha proxima audiencia",
    r"qual e a proxima audiencia",
    r"me informe sobre minhas proximas audiencias",
    r"teremos no mes de dezembro",
    r"agendadas para dezembro",
    
    r"programadas para o proximo mes",
    r"para o mes de dezembro",
    r"teremos em dezembro",
    r"previstas para dezembro",
    r"confirmadas para o mes de dezembro",
    r"agendadas para dezembro",
    r"sessoes de audiencia teremos no proximo mes",
    r"numero de audiencias que teremos no mes de dezembro",
    r"previstas para acontecer em dezembro",
    r"audiencias estao programadas para dezembro",
    r"confirmadas para o mes de dezembro",
    r"audiencias estao na agenda para dezembro"
]

categoria_perguntas['estado_maior_media_valor_causa'] = [
    r"estado com maior media de valor da causa",
    r"qual estado tem a maior media da causa",
    r"qual estado tem a maior media de causa",
    r"qual a maior media de causa por estado",
    r"estado com a maior media de valor de causa",
    r"maior media de valor de causa por estado",
    r"qual estado teve a maior media de causas",
    r"media mais alta de causas por estado"
]

categoria_perguntas['divisao_resultados_processos'] = [
    r"divisao dos resultados dos processos",
    r"como estao divididos os resultados",
    r"divisao dos processos por resultado",
    r"resultados dos processos divididos",
    r"divisao de processos",
    r"resultados de processos",
    r"como estao os resultados dos processos",
    r"dividir resultados dos processos"
]

categoria_perguntas['transitaram_julgado'] = [
    r"processos que transitaram em julgado",
    r"quais processos transitaram em julgado",
    r"transitaram em julgado",
    r"quais processos ja transitaram em julgado",
    r"ja transitaram em julgado",
    r"processos transitados em julgado",
    r"quantos processos transitaram em julgado",
    r"numero de processos transitados"
]

categoria_perguntas['quantidade_processos_estado'] = [
    r"quantidade de processos por estado",
    r"Divididos em quais estados",
    r"quantos processos existem em cada estado",
    r"numero de processos por estado",
    r"quantos processos por estado",
    r"processos por estado",
    r"processos em cada estado",
    r"quantos processos ha por estado",
    r"processos divididos por estado",
    r"Divididos em quais estados",
    r"quais estados os processos estao divididos",
    r"estados em que os processos estao distribuidos",
    r"informar em quais estados",
    r"divididos entre quais estados",
    r"estados ha processos",
    r"quais estados os processos estao",
    r"estados possuem processos cadastrados",
    r"que estados os processos estao",
    r"listar os estados onde ha processos ativos",
    r"quais estados os processos",
    r"distribuicao dos processos por estado",
    r"quais estados estao os processos",
    r"divisao dos processos entre os estados",
    r"estados ha processos na base",
    r"lista de estados com processos"

]

categoria_perguntas['quantidade_processos_comarca'] = [
    r"quantidade de processos por comarca",
    r"quantos processos existem em cada comarca",
    r"numero de processos por comarca",
    r"quantos processos por comarca",
    r"processos por comarca",
    r"processos em cada comarca",
    r"quantos processos ha por comarca",
    r"processos divididos por comarca"
]

categoria_perguntas['quantidade_total_processos'] = [
    r"quantidade total de processos",
    r"quantos processos existem no total",
    r"quantos processos ao todo",
    r"total de processos",
    r"quantos processos existem",
    r"numero total de processos",
    r"processos no total",
    r"total de casos"
]

categoria_perguntas['valor_total_causa'] = [
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
    r"gostaria de saber quantos processos ativos",
    r"processos ativos eu tenho na base",
    r"pode me informar o numero de processos ativos",
    r" total de processos ativos",
    r"ativos na base hoje",
    r"consultar quantos processos ativos",
    r"processos estao ativos",
    r"numero atual de processos ativos",
    r"verificar quantos processos ativos",
    r"processos ativos na base ate agora",
    r"mostrar o total de processos ativos",
    r"registrados como ativos",
    r"contagem de processos ativos",
    r"processos ativos atualmente",
    r"processos ativos que tenho",
    r"dizer quantos processos ativos",
    r"conferir quantos processos estao ativos",
    r"conferir quantos processos ativos",
    r"quantidade atual de processos ativos",
    r"verificar quantos processos ativos existem",
    r"processos ativos foram registrados",
    r"saber o total de processos ativos",
    r"listar o numero de processos ativos",
    r"processos ativos estao disponiveis",
    r"confirmar o total de processos ativos",
    r"processos ativos cadastrados",
    r"processos ativos estao",
    r"numero mais recente de processos ativo",
    r"quantidade total de processos ativos",
    
    r"contagem atual de processos ativos",
    r"quantos processos ativos",
    r"processos ativos",
    r"quantos processos tenho ativos",
    r"numero de processos ativos",
    r"processos que estao ativos",
    r"quais processos estao ativos",
    r"numero de casos ativos",
    r"quais sao os processos ativos"
]

categoria_perguntas['processos_arquivados'] = [
    r"quantos processos arquivados",
    r"processos arquivados",
    r"numero de processos arquivados",
    r"quais processos foram arquivados",
    r"arquivamento de processos",
    r"processos ja arquivados",
    r"processos que ja foram arquivados",
    r"quantos casos arquivados"
]

categoria_perguntas['quantidade_recursos'] = [
    r"quantos recursos foram interpostos",
    r"numero de recursos interpostos",
    r"recursos interpostos",
    r"quantos recursos foram feitos",
    r"quantos recursos existem",
    r"numero total de recursos",
    r"recursos feitos",
    r"quantos recursos ja foram interpostos"
]

categoria_perguntas['sentencas'] = [
    r"divisao dos resultados das sentencas",
    r"divisao das sentencas",
    r"como estao divididos os resultados das sentencas",
    r"divisao das decisoes",
    r"sentencas divididas",
    r"quais foram as sentencas",
    r"resultados das sentencas",
    r"sentencas proferidas"
]

categoria_perguntas['valor_sentenca'] = [
    r"sentenca mais elevada",
    r"sentenca de maior valor",
    r"sentenca mais alta",
    r"sentenca mais significativa",
    r"sentenca de maior valor",
    r"recebeu a sentenca mais elevada",
    r"caso com uma sentenca mais alta",
    r"processo com a sentenca mais elevada",
    r"dizer qual caso tem a sentenca mais alta",
    r"sentenca de maior valor ate agora",
    r"conferir o caso com a sentenca mais elevada",
    r"sentenca mais alta registrada",
    r"maior valor de sentenca",
    r"maior sentenca",
    r"sentenca de valor mais alto",
    r"destaca pela sentenca",
    r"valor de sentenca aplicado",
    r"sentenca considerada a mais alta",
    r"sentenca mais elevada esta registrada",
    r"recebeu a sentenca mais alta",
    r"montante mais alto na sentenca",
    r"relevante em termos de valor de sentenca",
    r"decisao judicial mais elevada em valor",
    r"decisao de sentenca mais",
    r"sentenca de valor mais expressivo",
    r"recebeu a maior sentenca"
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
    r"quais tribunais tem mais acoes de convencoes coletivas",
    r"tribunal com mais casos sobre convencoes coletivas",
    r"quais tribunais tem mais convencoes coletivas",
    r"qual tribunal lida com mais convencoes coletivas",
    r"tribunal que tem mais casos de convencoes coletivas",
    r"quais tribunais tem mais acoes relacionadas a convencoes coletivas"
]

categoria_perguntas['rito_sumarisimo'] = [
    r"rito sumarisimo",
    r"processos no rito sumarissimo",
    r"quantos processos estao no rito sumarissimo",
    r"casos no rito sumarissimo",
    r"quais processos seguem o rito sumarissimo",
    r"quais casos estao no rito sumarissimo",
    r"numero de processos no rito sumarissimo",
    r"processos sumarissimos"
]

categoria_perguntas['divisao_fase'] = [ #???
    r"divisao por fase",
    r"como esta a divisao dos processos por fase",
    r"processos divididos por fase",
    r"qual e a divisao dos processos por fase",
    r"como estao os processos divididos por fase",
    r"fases dos processos",
    r"divisao dos processos por fase",
    r"quais sao as fases dos processos"
]

categoria_perguntas['reclamantes_multiplos'] = [
    r"algum reclamante tem mais de um processo",
    r"reclamantes com mais de um processo",
    r"tem algum reclamante com multiplos processos",
    r"reclamantes que possuem mais de um processo",
    r"quem tem mais de um processo",
    r"quais reclamantes tem mais de um processo",
    r"reclamantes com multiplos processos",
    r"reclamante com mais de um processo"
]

categoria_perguntas['estado_mais_ofensor'] = [
    r"estado devo ter mais preocupacao",
    r"estado mais ofensor",
    r"qual estado e o mais preocupante",
    r"em qual estado devo me preocupar mais",
    r"estado que mais ofende",
    r"estado mais preocupante",
    r"qual estado tem maior risco",
    r"estado com maior risco"
]

categoria_perguntas['comarca_mais_ofensora'] = [
    r"comarca devo ter mais preocupacao",
    r"comarca mais ofensora",
    r"qual comarca e a mais preocupante",##gemini
    r"comarca com maior risco",
    r"comarca mais arriscada",
    r"comarca com mais ofensas",
    r"qual comarca tem mais riscos",
    r"em qual comarca devo me preocupar mais"
]

categoria_perguntas['maior_media_duracao_estado'] = [
    r"estado com maior media de duracao",
    r"qual estado tem a maior media de duracao",
    r"qual estado tem maior duracao media",
    r"estado com maior duracao media",
    r"qual estado leva mais tempo para finalizar os processos",
    r"qual estado tem a maior media de tempo de processos",
    r"estado que leva mais tempo em processos",
    r"estado com a maior media de tempo em processos"
]

categoria_perguntas['maior_media_duracao_comarca'] = [
    r"comarca com maior media de duracao",
    r"qual comarca tem a maior media de duracao",
    r"qual comarca tem maior duracao media",
    r"comarca com maior duracao media",
    r"qual comarca leva mais tempo para finalizar os processos",
    r"qual comarca tem a maior media de tempo de processos",
    r"comarca que leva mais tempo em processos",
    r"comarca com a maior media de tempo em processos"
]

categoria_perguntas['processos_improcedentes'] = [
    r"quantos processos improcedentes",
    r"quantos processos improcedente",
    r"processos julgados improcedentes",
    r"quais os processos foram improcedentes",
    r"quais os processos foram improcedente",
    r"processos improcedentes",
    r"casos julgados improcedentes",
    r"numero de processos improcedentes"
]

categoria_perguntas['processos_procedentes'] = [
    r"quantos processos procedentes",
    r"processos julgados procedentes",
    r"quais os processos foram procedentes",
    r"quais os processos foram procedente",
    r"processos procedentes",
    r"casos julgados procedentes",
    r"numero de processos procedentes",
    r"quais casos foram procedentes"
]

categoria_perguntas['processos_extintos_sem_custos'] = [
    r"quantos processos extintos sem custos",
    r"processos extintos sem custos",
    r"processos sem custos extintos",
    r"quantos processos foram extintos sem custos",
    r"numero de processos extintos sem custos",
    r"processos extintos sem custos totais",
    r"quais processos foram extintos sem custos",
    r"extincao de processos sem custos"
]

categoria_perguntas['processo_maior_tempo_sem_movimentacao'] = [
    r"processo com maior tempo sem movimentacao",
    r"qual processo esta mais tempo sem movimentacao",
    r"processo que esta mais tempo parado",
    r"qual processo nao tem movimentacao ha mais tempo",
    r"qual o processo mais parado",
    r"processo sem movimentacao ha mais tempo",
    r"processo com maior tempo parado",
    r"qual o processo com maior inatividade"
]

categoria_perguntas['divisao_por_rito'] = [
    r"como esta a divisao por rito", ## quem respondeu foi o gemini
    r"qual a divisao dos processos por rito",
    r"como e a divisao por rito dos processos",
    r"processos divididos por rito",
    r"qual e a divisao dos processos por rito",
    r"quais sao os ritos dos processos",
    r"processos por rito",
    r"como estao os processos divididos por rito"
]

categoria_perguntas['processos_nao_julgados'] = [
    r"quantos processos ainda nao foram julgados",
    r"processos nao julgados",
    r"quais processos ainda nao foram julgados",
    r"numero de processos nao julgados",
    r"quais casos ainda nao foram julgados",
    r"processos pendentes de julgamento",
    r"processos que ainda nao foram julgados",
    r"quantos casos nao foram julgados"
]

categoria_perguntas['processos_nao_citados'] = [ #erro
    r"quantos processos ainda nao foram citados",
    r"processos nao citados",
    r"quais processos ainda nao foram citados",
    r"numero de processos nao citados",
    r"quais casos ainda nao foram citados",
    r"processos pendentes de citacao",
    r"processos que ainda nao foram citados",
    r"quantos casos nao foram citados"
]

categoria_perguntas['processo_mais_antigo'] = [
    r"processo mais antigo da base",
    r"qual o processo mais antigo",
    r"qual e o processo mais antigo",
    r"processo mais antigo",
    r"qual caso e o mais antigo",
    r"caso mais antigo",
    r"numero do processo mais antigo",
    r"quais sao os processos mais antigos"
]

categoria_perguntas['classe_cnj'] = [
    r"quantos sao trabalhistas",
    r"quantos sao civeis",
    r"quantos sao penais"
    r"quantos sao trabalhista",
    r"processos sao trabalhistas",
    r"quantos processos trabalhistas",
    r"numero de processos trabalhistas",
    r"processos ativos sao trabalhistas",
    r"quantos processos trabalhistas",
    r"quantidade de processos trabalhistas",
    r"natureza trabalhista",
    r"consultar quantos processos trabalhistas",
    r"processos trabalhistas temos",
    r"total de processos trabalhistas",
    r"quantos processos sao trabalhistas",
    r"cadastrados sao trabalhistas",
    r"dizer o numero de processos trabalhistas",
    r"verificar quantos processos sao da area trabalhista",
    r"quantidade de processos trabalhistas"
]

