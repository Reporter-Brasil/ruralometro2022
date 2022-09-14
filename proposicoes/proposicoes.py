# -*- coding: utf-8
# Repórter Brasil (https://ruralometro2022.reporterbrasil.org.br/)
# Reinaldo Chaves (@paidatocandeira)
# Script que procura na API da Câmara dos Deputados (2000-2021) as proposições legislativas de interesse de interesse ambiental e social
# API - https://dadosabertos.camara.leg.br/swagger/api.html

import requests
import json
import pandas as pd
import xmltodict


# Procura dados para preparacao
headers = {
    'accept': 'application/xml',
}

# parametros com intervalo de datas previsto
params = (
    ('dataApresentacaoInicio', '2000-01-01'),
    ('dataApresentacaoFim', '2021-11-17'),
    ('ordem', 'ASC'),
    ('ordenarPor', 'id'),
    ('formato', 'json'),
    ('itens', 100),
)

response = requests.get('https://dadosabertos.camara.leg.br/api/v2/proposicoes', headers=headers, params=params)

# pega última proposicao
for vez in response.json()['links']:
	conta = {"rel": vez['rel'].strip(), "href": vez['href'].strip()}

print(conta)

# pega último link
link_ultimo = str(conta['href'].strip())
print(link_ultimo)

# cria variável com último item
ultima = 5924

#url base
url = "https://dadosabertos.camara.leg.br/api/v2/proposicoes?dataApresentacaoInicio=2000-01-01&dataApresentacaoFim=2021-11-17"



proposicoes = []

try:

	# Faz a iteração a partir do número de páginas encontrado
	for pagina in range(1, ultima):
		print(pagina)
		parametros = {'formato': 'json', 'itens': 100, 'pagina': pagina}
    	resposta = requests.get(url, parametros)

		# Captura os dados
    	for vez in resposta.json()['dados']:
    		dicionario = {"id": str(vez['id']).strip(), 
                          "uri": str(vez['uri']).strip(), 
                          "siglaTipo": str(vez['siglaTipo']).strip(), 
                          "codTipo": str(vez['codTipo']).strip(), 
                          "numero": str(vez['numero']).strip(), 
                          "ano": str(vez['ano']).strip(), 
                          "ementa": str(vez['ementa']).strip()
                          }
    		proposicoes.append(dicionario)
except:
	print("Erro: ", pagina)
	pass

df_proposicoes_api = pd.DataFrame(proposicoes)
df_proposicoes_api.info()

df_proposicoes_api.to_csv('proposicoes_2000_2021.csv', index=False)




df_proposicoes_api = pd.read_csv('proposicoes_2000_2021.csv', encoding ='utf-8', dtype = 'str', sep = ',')
df_proposicoes_api.info()


df_proposicoes_api['ementa_copia'] = df_proposicoes_api['ementa']
df_proposicoes_api['ementa_copia'] = df_proposicoes_api['ementa_copia'].str.upper()



palavras = pd.read_excel('palavras_meio_ambiente.xlsx', sheet_name = 'Planilha1', dtype = 'str')
palavras


palavras['palavras_upper'] = palavras['palavras'].str.upper()
palavras



lista_palavras = palavras['palavras_upper'].tolist()
lista_palavras



# Procura por palavras
df_proposicoes_api_filtra = df_proposicoes_api[pd.notnull(df_proposicoes_api['ementa_copia'])].copy()
mask = df_proposicoes_api_filtra['ementa_copia'].str.contains('|'.join(lista_palavras))
seleciona = df_proposicoes_api_filtra[mask]


seleciona.info()








# Busca a última situação das proposicoes
endpoint = "https://dadosabertos.camara.leg.br/api/v2/proposicoes/"

projetos = []
parametros = {'formato': 'json'}

for num, row in seleciona.iterrows():
  id = row['id']

  url = endpoint + id
  print(url)

  # captura os dados de detalhes
  try:
    r = requests.get(url, parametros)

    vez =  r.json()['dados']
    
    dicionario = {"id": str(vez['id']).strip(), 
        	          "uri": str(vez['uri']).strip(), 
                          "siglaTipo": str(vez['siglaTipo']).strip(), 
                          "codTipo": str(vez['codTipo']).strip(), 
                          "numero": str(vez['numero']).strip(), 
                          "ano": str(vez['ano']).strip(), 
                          "ementa": str(vez['ementa']).strip(),
                          "dataApresentacao": str(vez['dataApresentacao']).strip(),
                          "statusProposicao_dataHora": str(vez['statusProposicao']['dataHora']).strip(),
                          "statusProposicao_siglaOrgao": str(vez['statusProposicao']['siglaOrgao']).strip(),
                          "statusProposicao_siglaOrgao": str(vez['statusProposicao']['siglaOrgao']).strip(),
                          "statusProposicao_descricaoTramitacao": str(vez['statusProposicao']['descricaoTramitacao']).strip(),
                          "statusProposicao_descricaoSituacao": str(vez['statusProposicao']['descricaoSituacao']).strip(),
                          "statusProposicao_despacho": str(vez['statusProposicao']['despacho']).strip(),
                          "keywords": str(vez['keywords']).strip(),
                          "urlInteiroTeor": str(vez['urlInteiroTeor']).strip(),
                          "uriAutores": str(vez['uriAutores']).strip()
                          }
    projetos.append(dicionario)
  except:
  	print("ERRRO: ", url)

df_proposicoes_situacao = pd.DataFrame(projetos)


df_proposicoes_situacao.info()

df_proposicoes_situacao.to_csv('autores_proposicoes_2000_2021_por_assuntos_sem_filtrar_nomes_com_situacao_23_nov.csv', index=False)



# Carrega proposicoes + situacao
df_proposicoes_situacao = pd.read_csv('autores_proposicoes_2000_2021_por_assuntos_sem_filtrar_nomes_com_situacao_23_nov.csv', encoding ='utf-8', dtype = 'str', sep = ',')
df_proposicoes_situacao.info()




# Coleta autores totais
endpoint = "https://www.camara.leg.br/SitCamaraWS/Proposicoes.asmx/ListarAutoresProposicao?codProposicao="

conta = 0

for num, row in df_proposicoes_situacao.iterrows():
  id = row['id']

  url = endpoint + id
  print(url)

  try:
    r = requests.get(url)
  except requests.exceptions.RequestException as e:
    print("Requests exception: {}".format(e))

  try:
    jsonString = json.dumps(xmltodict.parse(r.text), indent=4)

    d = json.loads(jsonString)

    lista = [d['autores']]

    df_lista = pd.DataFrame(lista)
    df_lista["id"] = id
  except:
    print("Erro: ", url)
    df_lista = pd.DataFrame({'autor': 'erro', 'id': id, 'subscritores': 'erro'}, index=[0])
    
  if conta == 0:
    df_autores = df_lista.copy()
  else:
    df_autores = df_autores.append(df_lista)

  conta = conta + 1

df_autores.info()


df_proposicoes_situacao_autores = pd.merge(df_proposicoes_situacao, df_autores, left_on='id', right_on='id')
df_proposicoes_situacao_autores.info()


df_proposicoes_situacao_autores.to_csv('autoresgeral_proposicoes_2000_2021_por_assuntos_sem_filtrar_nomes_com_situacao_23_nov.csv', index=False)


df_proposicoes_situacao_autores = pd.read_csv('autoresgeral_proposicoes_2000_2021_por_assuntos_sem_filtrar_nomes_com_situacao_23_nov.csv', encoding ='utf-8', dtype = 'str', sep = ',')
df_proposicoes_situacao_autores.info()



# Carrega dados dos deputados
deputados = pd.read_csv('ids_deputados_2018.csv', encoding ='utf-8', dtype = 'str', sep = ',')
deputados['uri'] = deputados['uri'].str.strip()
deputados.info()


procura_nomes = []
parametros = {'formato': 'json'}
for num, row in df_proposicoes_situacao_autores.iterrows():
  link = row['uriAutores']
  id = row['id']
  print(link)
  filtra = ""

  try:
    r = requests.get(link, parametros)

    for vez in r.json()['dados']:
      procura = vez['uri'].strip()

      filtra = deputados[(deputados['uri'] == procura)].copy()

      if filtra.empty is False:
        procura_nomes.append(id)
  except:
    print("ERRRO: ", link)


procura_nomes

# elimina duplicados
procura_nomes_final = list(set(procura_nomes))
procura_nomes_final

# transforma em dataframe
df_procura_nomes_final = pd.DataFrame(procura_nomes_final, columns = ['id'])
df_procura_nomes_final.info()


# cruza e deixa apenas proposicoes de deputados de 2018 - pelo id da proposicao
df_proposicoes_final = pd.merge(df_proposicoes_situacao_autores, df_procura_nomes_final, left_on='id', right_on='id')
df_proposicoes_final.info()


prefixo = "https://www.camara.leg.br/propostas-legislativas/" 
df_proposicoes_final['site_proposicao'] = [prefixo + str(row) for row in df_proposicoes_final['id']]

df_proposicoes_final.to_csv('proposicoes_meioambiente_23_nov_rodado2022.csv', index=False)

df_proposicoes_final.to_excel('proposicoes_meioambiente_23_nov_rodado2022.xlsx',sheet_name='Sheet1')


