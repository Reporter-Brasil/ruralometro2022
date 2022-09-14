# -*- coding: utf-8
# Repórter Brasil (https://ruralometro2022.reporterbrasil.org.br/)
# Reinaldo Chaves (@paidatocandeira)
# Script para acessar a API da Câmara dos Deputados e pegar dados de deputados eleitos em 2018

import requests
import json
import pandas as pd
import xmltodict
import unidecode


# Função para retirar acentuação
def f(str):
    return (unidecode.unidecode(str))



# Captura API de deputados
url = 'https://dadosabertos.camara.leg.br/api/v2/deputados'

deputados = []
for pagina in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
  parametros = {'formato': 'json', 'itens': 100, 'pagina': pagina}
  resposta = requests.get(url, parametros)
  for deputado in resposta.json()['dados']:
    dicionario = {"deputado": deputado['nome'], "link_api": deputado['uri']}
    deputados.append(dicionario)
df_deputados_api = pd.DataFrame(deputados)
df_deputados_api.info()



# Captura dados de deputados
deputados_dados = []

for num, row in df_deputados_api.iterrows():
	url = (row['link_api'])
	print(url)

  deputado = (row['deputado'])
  #print('deputado: ' + deputado)
  parametros = {'formato': 'json'}
  resposta = requests.get(url, parametros)

  dicionario = {"deputado_id": str(resposta.json()['dados']['id']),
                      "nome_completo": resposta.json()['dados']['nomeCivil'],
                      "uri": url, 
                      "partido": resposta.json()['dados']['ultimoStatus']['siglaPartido'],
                      "legislatura": resposta.json()['dados']['ultimoStatus']['idLegislatura'],
                      "nome_urna": resposta.json()['dados']['ultimoStatus']['nomeEleitoral'],
                      "url_foto": resposta.json()['dados']['ultimoStatus']['urlFoto'],
                      "data_nascimento": resposta.json()['dados']['dataNascimento'],
                      "situacao": resposta.json()['dados']['ultimoStatus']['situacao'],
                      "condicao": resposta.json()['dados']['ultimoStatus']['condicaoEleitoral']}
  deputados_dados.append(dicionario)

deputados_dados_api = pd.DataFrame(deputados_dados)
deputados_dados_api["nome_completo"] = deputados_dados_api["nome_completo"].apply(f)

deputados_dados_api

deputados_dados_api['condicao'].unique()
deputados_dados_api.info()




# Deputados eleitos em 2018
# Inclui DAVID MICHAEL DOS SANTOS MIRANDA
df_2018 = pd.read_csv('consulta_cand_2018_BRASIL.csv', encoding ='latin_1', dtype = 'str', sep = ';')
df_2018['DS_SIT_TOT_TURNO'].unique()
df_2018_deputados = df_2018[(df_2018['DS_CARGO'] == 'DEPUTADO FEDERAL')]
df_2018_deputados = df_2018_deputados[(df_2018_deputados['DS_SIT_TOT_TURNO'] == 'ELEITO POR MÉDIA')|
                                      (df_2018_deputados['DS_SIT_TOT_TURNO'] == 'ELEITO POR QP') |
                                      (df_2018_deputados['NR_CPF_CANDIDATO'] == '12394073780') 
                                      ]
df_2018_deputados.shape
df_2018_deputados_nomes = df_2018_deputados[['NM_CANDIDATO', 'NR_CPF_CANDIDATO']]






#Comparação com os nomes completos das bases
df_eleitos = pd.merge(df_2018_deputados_nomes, deputados_dados_api, left_on='NM_CANDIDATO', right_on='nome_completo')
df_eleitos.info()



# Procura nomes que faltaram
nomes_naoeleitos = pd.merge(df_2018_deputados_nomes, 
                        deputados_dados_api, 
                        left_on='NM_CANDIDATO', 
                        right_on='nome_completo',
                        how='outer',
                        indicator=True)
# Agrupa apenas pelo lado esquerdo - a lista do TSE
ldf = nomes_naoeleitos.query("_merge == 'left_only'").drop('_merge',axis=1)
ldf.info()
ldf.to_csv('resultados/deputados_nao_encontrados.csv', index=False)


#Nesse ponto fiz uma checagem manual dos 158 nomes, adicionado a coluna chave que acessa a API de cada deputado
deputados_restantes = pd.read_excel('resultados/deputados_nao_encontrados.xlsx',sheet_name='deputados_nao_encontrados (1)')
deputados_restantes.info()

restantes = []

# Apenas WAGNER MONTES DOS SANTOS dá erro
# Morreu um pouco depois da posse e não entrou no sistema da Câmara
# No lugar entrou JORGE BRAZ DE OLIVEIRA
# E entrou DAVID MICHAEL DOS SANTOS MIRANDA no lugar JEAN WYLLYS DE MATOS SANTOS

for num, row in deputados_restantes.iterrows():
  try:
    url = str((row['chave_api']))
    #url = 'https://dadosabertos.camara.leg.br/api/v2/deputados/' + chave
    deputado = (row['NM_CANDIDATO'])
    cpf = (row['NR_CPF_CANDIDATO'])
    print('deputado: ' + deputado)
    parametros = {'formato': 'json'}
    resposta = requests.get(url, parametros)
    dicionario = {"NM_CANDIDATO": deputado,
                   "NR_CPF_CANDIDATO": cpf,
                     "deputado_id": str(resposta.json()['dados']['id']),
                      "nome_completo": resposta.json()['dados']['nomeCivil'],
                      "uri": url, 
                      "partido": resposta.json()['dados']['ultimoStatus']['siglaPartido'],
                      "legislatura": resposta.json()['dados']['ultimoStatus']['idLegislatura'],
                      "nome_urna": resposta.json()['dados']['ultimoStatus']['nomeEleitoral'],
                      "url_foto": resposta.json()['dados']['ultimoStatus']['urlFoto'],
                      "data_nascimento": resposta.json()['dados']['dataNascimento'],                      
                      "situacao": resposta.json()['dados']['ultimoStatus']['situacao'],
                      "condicao": resposta.json()['dados']['ultimoStatus']['condicaoEleitoral']}
    restantes.append(dicionario)
  except:
    print("Erro: ", deputado)
    pass

restantes_api = pd.DataFrame(restantes)
restantes_api.info()


# Cria o conjunto final de 513 deputados
frames = [df_eleitos, restantes_api]
deputados_2018 = pd.concat(frames)
deputados_2018.info()


# Retira nomes que não vão entrar de acordo com a metodologia
# Jean Wyllys, FRANCISCO DE ASSIS CARVALHO GONÇALVES, LUIZ FLAVIO GOMES e JOSE CARLOS SCHIAVINATO
values_list = ["59919230510", "15670961315", "70641218834", "27696090925"]

deputados_2018_final = deputados_2018[~deputados_2018['NR_CPF_CANDIDATO'].isin(values_list)]

deputados_2018_final.info()


deputados_2018_final.to_csv('ids_deputados_2018_abril_2022.csv', index=False)

 


### Faz coleta final de abril de 2022
abril22 = pd.read_excel('resultados/abril_testepoliticos.xlsx', sheet_name = 'Sheet1', dtype = 'str')
abril22.info()



abril = []

for num, row in abril22.iterrows():
  try:
    url = str((row['uri_x']))
    
    cpf = (row['NR_CPF_CANDIDATO'])
    deputado = (row['NM_CANDIDATO_x'])
    print('deputado: ' + deputado)

    parametros = {'formato': 'json'}
    resposta = requests.get(url, parametros)

    dicionario = {"NM_CANDIDATO": deputado,
                   "NR_CPF_CANDIDATO": cpf,
                     "deputado_id": str(resposta.json()['dados']['id']),
                      "nome_completo": resposta.json()['dados']['nomeCivil'],
                      "uri": url, 
                      "partido": resposta.json()['dados']['ultimoStatus']['siglaPartido'],
                      "uf_eleicao_disputa": resposta.json()['dados']['ultimoStatus']['siglaUf'],
                      "legislatura": resposta.json()['dados']['ultimoStatus']['idLegislatura'],
                      "nome_urna": resposta.json()['dados']['ultimoStatus']['nomeEleitoral'],
                      "url_foto": resposta.json()['dados']['ultimoStatus']['urlFoto'],
                      "data_nascimento": resposta.json()['dados']['dataNascimento'],                      
                      "situacao": resposta.json()['dados']['ultimoStatus']['situacao'],
                      "condicao": resposta.json()['dados']['ultimoStatus']['condicaoEleitoral']}
    abril.append(dicionario)
  except:
    print("Erro: ", deputado)
    pass

abril_api = pd.DataFrame(abril)
abril_api.info()



abril_api.to_csv('ids_deputados_2018_versao_abril_2022.csv', index=False)