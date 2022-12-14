[![Ruralômetro](doc/índice.jpeg)](https://ruralometro2022.reporterbrasil.org.br/)

----
 O [Ruralômetro](https://ruralometro2022.reporterbrasil.org.br) é um banco de dados e uma ferramenta interativa que avalia a atuação dos deputados federais nas questões ligadas ao meio ambiente, trabalhadores rurais, povos indígenas e outras comunidades tradicionais. Nesta segunda edição do projeto, são avaliados os parlamentares que tomaram posse no início de 2019. Desenvolvida pela Repórter Brasil com uma equipe multidisciplinar, a ferramenta usa duas bases de dados para pontuar os parlamentares: seu posicionamento na votação de projetos de lei e medidas provisórias que apresentam algum impacto socioambiental e as proposições apresentadas por cada um nesta atual legislatura.

Foram convidadas para avaliar o mérito de cada proposta 22 organizações não-governamentais. Elas classificaram os projetos votados e apresentados como favoráveis ou desfavoráveis para o meio ambiente e as populações do campo. Todas são referência nas áreas em que atuam e executaram a tarefa voluntariamente – motivo pelo qual este projeto lhes deve sinceros agradecimentos. São elas:

Articulação dos Povos Indígenas do Brasil (Apib), Associação Brasileira de Reforma Agrária (Abra), Associação das Comunidades Quilombolas do Estado do Rio de Janeiro (Acquilerj), Comissão Pastoral da Terra (CPT), Comissão Pró-Índio de São Paulo, Conectas Direitos Humanos, Confederação Nacional dos Trabalhadores Assalariados e Assalariadas Rurais (Contar), Confederação Nacional dos Trabalhadores Rurais Agricultores e Agricultoras Familiares (Contag), Conselho Indigenista Missionário (Cimi), Federação de Órgãos para Assistência Social e Educacional (Fase), Greenpeace Brasil, Instituto Brasileiro de Defesa do Consumidor (Idec), Instituto de Energia e Meio Ambiente (IEMA), Instituto Democracia e Sustentabilidade (IDS), Instituto Socioambiental (ISA), International Rivers, KOINONIA Presença Ecumênica e Serviço, Movimento dos Atingidos por Barragens (MAB), Observatório da Mineração, Observatório do Clima, Observatório do Código Florestal e WWF Brasil.

Cada deputado ganhou uma pontuação individual, que leva em conta os projetos que ele votou ou propôs. Essa pontuação foi aplicada à escala de temperatura corporal humana: quanto mais projetos com impacto negativo o deputado votou ou propôs, mais alta é sua temperatura, podendo chegar a níveis de febre.

A escala varia entre 36ºC e 42ºC. A temperatura de 37,3ºC é considerada neutra. Valores menores que esse indicam os parlamentares que tiveram uma atuação dentro da Câmara considerada favorável na temática socioambiental. Acima dessa temperatura, o desempenho foi desfavorável.

Além do cálculo da temperatura, o Ruralômetro reúne outros dados que podem influenciar a atuação política do parlamentar ou que são de interesse público, como as infrações ambientais e trabalhistas que ele e seus financiadores cometeram. Essas e outras informações adicionais são mostradas no gráfico por meio de filtros de visualização (leia mais sobre os filtros na [metodologia](https://ruralometro2022.reporterbrasil.org.br/metodologia)).

O Ruralômetro também possui páginas que apresentam as seleções de 28 votações nominais ocorridas na Câmara e de quase 500 propostas apresentadas pelos deputados na atual legislatura e que têm impacto no campo socioambiental. Além disso, o site traz ainda uma série de reportagens analisando os dados recolhidos.

Ao revelar e cruzar essas informações, o Ruralômetro faz um raio-x da atuação da Câmara no atual governo e oferece uma ferramenta de pesquisa para a campanha eleitoral de 2022, já que muitos desses parlamentares concorrerão à reeleição ou a outros cargos no pleito deste ano. 

O Github do Ruralômetro 2022 apresenta os programas que foram utilizados para extrair e analisar os dados. Os programas são em Python 3.8 (foi utilizado Jupyter Notebook e scripts .py)

O repositório do projeto em 2018 está [aqui](https://github.com/Reporter-Brasil/Ruralometro)

----
 ### DEPUTADOS
É o script para acessar a API da Câmara dos Deputados e pegar dados de deputados eleitos em 2018. Contém também arquivo final gerado na extração final de 2022 de acordo com nossa [metodologia](https://ruralometro2022.reporterbrasil.org.br/metodologia)

### PROPOSIÇÕES
Script que procura na API da Câmara dos Deputados (2000-2021) as proposições legislativas de interesse de interesse ambiental e social, de acordo com nossa [metodologia](https://ruralometro2022.reporterbrasil.org.br/metodologia) - procura nas ementas das proposições, a partir de palavras-chave definidas. E depois inclui no mesmo dataframe todos os autores - e separa os deputados de 2018

### DOAÇÕES
Cruza os deputados eleitos em 2018 com os dados de doações informados ao TSE para gerar os arquivos gerais de doações diretas, indiretas e originárias

### EMBARGOS
Faz o cruzamento de deputados e doações - para saber deputados que podem estar nos embargos do Ibama ou doadores que estão na lista de embargos

### AUTOS IBAMA
Faz o cruzamento de deputados e doações - para saber deputados que podem estar nos autos de infração do Ibama ou doadores que estão na lista de autos

### AUTOS ICMBIO
Faz o cruzamento de deputados e doações - para saber deputados que podem estar nos autos de infração do ICMBio ou doadores que estão na lista de autos

### AUTOS TRABALHISTAS
Faz o cruzamento de deputados e doações - para saber deputados que podem estar nos autos de infração trabalhista do antigo Ministério do Trabalho ou doadores que estão na lista de autos

### TRABALHO ESCRAVO
Faz o cruzamento de deputados e doações - para saber deputados que podem estar no Cadastro de Empregadores que tenham submetido trabalhadores a condições análogas à de escravo ou doadores que estão na lista - não encontrou

### BANCADA RURALISTA
Faz cruzamento de nomes para marcar deputados que fazem parte da Frente Parlamentar da Agropecuária - FPA

### EMPRESAS NA RECEITA FEDERAL
Faz o cruzamento de nomes completos e CPFs de deputados com os dados da Receita Federal para obter empresas (ativas e inativas) que os deputados participam do quadro de sócios e administradores (QSA) e também os demais sócios dessas empresas e os outros CNPJs que eles possuem

### EMBARGOS DO IBAMA EMPRESAS
Procura empresas de deputados federais inscritas em embargos do Ibama

### AUTOS DO IBAMA EMPRESAS
Procura empresas de deputados federais inscritas em autos de infração do Ibama

### AUTOS DO ICMBIO EMPRESAS
Procura empresas de deputados federais inscritas em autos de infração do ICMBio

### AUTOS TRABALHISTAS EMPRESAS
Procura empresas de deputados federais inscritas em autos de infração trabalhista do antigo Ministério do Trabalho

### EMPRESAS DE DEPUTADOS COM CNAE DE INTERESSE
Filtra as empresas de deputados, ativas e inativas e que aparecem no quadro de sócios e administradores (QSA), que possuem Classificação Nacional de Atividades Econômicas – CNAE com atividades relacionadas à agricultura ou extração que envolva questões ambientais

### MULTAS DE EMPRESAS DE DOADORES
Lista os IDs dos doadores de deputados inscritos nas listas de irregularidades do projeto, eliminando repetições. Lista as empresas dos doadores, a partir dos IDs. Verifica se as empresas estão nas listas de irregularidades

### VOTAÇÕES
Captura as informações de votações nominais parlamentares escolhidas no Ruralômetro. Dados vindos da API da Câmara

### AUTORES DE PROPOSIÇÕES
Captura as informações de autores de proposições legislativas escolhidas no Ruralômetro. Dados vindos da API da Câmara

### SOMA DOAÇÕES
Scripts para somar, sem repetições as doações dos deputados em 2018 - relacionadas às listas de pessoas/empresas no Ibama/ICMBio/infrações trabalhistas, e também separa as doações em geral de cada candidato analisado pelo projeto

### TEMPERATURA
A partir da metodologia do projeto (https://ruralometro2022.reporterbrasil.org.br/metodologia), que avalia os deputados a partir de critérios e atribui notas, este script cruza os resultados com o id_interno da Câmara para criar um banco de dados único



-------


equipe

COORDENAÇÃO Gisele Lobato e Ana Magalhães

EDIÇÃO Gisele Lobato, Ana Magalhães e Diego Junqueira

PESQUISA Guilherme Zocchio e Gisele Lobato

REPORTAGEM Diego Junqueira, Marina Rossi, Daniel Camargos, Joyce Cardoso, Gisele Lobato, Pedro Rocha Franco, Hélen Freitas e Ariene Susui

PROCESSAMENTO DE DADOS Reinaldo Chaves

ANÁLISE DE DADOS Marina Gama Cubas e Reinaldo Chaves

CONSULTORIA ESTATÍSTICA Simone Harnik

PROJETO GRÁFICO Studio Cubo Web

PROGRAMAÇÃO Paulo Campos e André Mota (Studio Cubo Web)

REDES SOCIAIS E DIVULGAÇÃO Tamyres Matos, Joyce Cardoso, Mariana Della Barba e Disarme Grafico (Bruno Ventura, Andressa Liebermann, Bruno Gentil, Daniel Ventura, Marina Hirakawa, Alex Mota, Diego Gomes e Saulo Castro)

ASSESSORIA DE IMPRENSA Elenita Fogaça Comunicação
