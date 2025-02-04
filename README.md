# Web Scrapping Stardew Valley
## Objetivo

Extrair, organizar e analisar dados das tabelas da wiki do Stardew Valley, com o objetivo de criar um conjunto de dados estruturados para futuras análises e visualizações.

## Tecnologias

- Request: Para realizar as requisições HTTP e baixar o conteúdo das páginas da wiki.
- Beautiful Soup: Para analisar o HTML das páginas e extrair as informações das tabelas.
- Python: Linguagem de programação utilizada para todo o desenvolvimento do projeto.

## Estrutura do Projeto

- extract_bs4.py: Extrai o html das páginas da Wiki da Stardle Valley e salva na pasta docs_raw.
- process_html_to_csv.py: Extrai as tabelas do html e transforma em csv na pasta docs_bronze.
- enrich_and_compile_csv.py: ETL e concatena csvs da pasta docs_bronze e salva na pasta docs_silver prontos para utilização de dashboards.
- dataviz.py: Projeto de carregar em página de internet utilizando a biblioteca Streamlit.
- docs_raw: Pasta para armazenar os arquivos HTML baixados da wiki.
- docs_bronze: Pasta para armazenar os arquivos CSV gerados na fase inicial de transformação dos dados.
- docs_silver: Pasta para armazenar os arquivos CSV com os dados concatenados e tratados.
- .env: Arquivo de configuração para armazenar credenciais e outras informações sensíveis.


## Etapas do Projeto

### `FASE 0 - configuração` :ok: 
Configuração do ambiente de desenvolvimento e criação do arquivo .env.

### `FASE 1 - Web Scraping:` :ok: 
Download de todas as tabelas de interesse da wiki do Stardew Valley e salvamento em arquivos HTML na pasta 'docs_raw'.

### `FASE 2 - Migração` :ok:
Transformação do notebook Jupyter(.ipynb) com o código de scraping em um script Python (.py) para facilitar a execução e manutenção.

### `FASE 3 - Transformação inicial` :ok:
- Leitura dos arquivos HTML e extração das tabelas utilizando Beautiful Soup.
- Conversão das tabelas para o formato CSV e salvamento na pasta 'docs_bronze'.

### `FASE 4 - Concatenação e tratamento` :construction_worker:
- Carregamento dos arquivos CSV da pasta 'docs_bronze'.
- Concatenação das tabelas com os mesmos tipos de dados.
- Limpeza e tratamento dos dados, como remoção de duplicados, tratamento de valores ausentes e formatação de dados.
- Salvamento das tabelas tratadas na pasta 'docs_silver'.

### `FASE 5 - Enriquecimento e Exportação` :construction_worker:
- Realização de análises exploratórias e enriquecimento dos dados, se necessário.
- Exportação dos dados para o GitHub em um formato adequado para compartilhamento e colaboração.
- Expansão do Conjunto de Dados: Incluir novas tabelas da wiki ou de outras fontes.
- Melhoria da Qualidade dos Dados: Implementar técnicas mais avançadas de limpeza e tratamento de dados.
- Análise Exploratória: Realizar análises mais profundas para descobrir insights interessantes sobre o jogo.
- Modelagem de Dados: Criar um modelo de dados mais elaborado para representar as informações de forma mais precisa.
- Integração com Ferramentas Externas: Integrar o projeto com outras ferramentas, como bancos de dados ou ferramentas de visualização.

### `FASE 6 - Visualização` :construction_worker:
- Criação de um dashboard interativo para visualizar os dados de forma clara e concisa.
- Criação de uma tech tree de produtos.
- Gerar cartas de cada item do banco de dados.

### `FASE 7 - ícones` :crystal_ball:
Importar biblioteca de imagens e ícones.