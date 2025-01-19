def profissoes ():
  import pandas as pd
  #profissões
  # renomear coluna 11
  profissao_cultivo = pd.read_csv('docs_bronze\profissao_cultivo.csv')
  profissao_coleta = pd.read_csv('docs_bronze\profissao_coleta.csv')
  profissao_mineracao = pd.read_csv('docs_bronze\profissao_mineracao.csv')
  profissao_pesca = pd.read_csv('docs_bronze\profissao_pesca.csv')
  profissao_combate = pd.read_csv('docs_bronze\profissao_combate.csv')

  # define nome das colunas
  cols = ['','nivel1', 'nivel2', 'nivel3', 'nivel4', 'nivel5',
        'nivel5.1', 'nivel6', 'nivel7', 'nivel8', 'nivel9', 'nivel10', 
        'nivel10.1', 'profissao']
  
  profissao_cultivo.columns = cols
  profissao_coleta.columns = cols
  profissao_mineracao.columns = cols
  profissao_pesca.columns = cols
  profissao_combate.columns = cols


  #concatenar dataframes profissões
  df_profissoes = pd.concat([profissao_cultivo,
                            profissao_pesca,
                            profissao_mineracao,
                            profissao_coleta,
                            profissao_combate], join='inner')#, ignore_index=True)


  # trazer a coluna profissao para o início:
  df_profissoes = df_profissoes[['profissao', 'nivel1', 'nivel2', 'nivel3', 'nivel4', 'nivel5', 'nivel5.1', 'nivel6', 'nivel7', 'nivel8', 'nivel9', 'nivel10', 'nivel10.1']]

  df_profissoes = df_profissoes.reset_index()
  df_profissoes = df_profissoes.drop(df_profissoes.columns[0], axis=1)

  df_profissoes.to_csv('docs_silver/profissoes.csv')

  print

  pass

def limpar_csv(arquivo):

  import re
  
  with open(arquivo, mode='r') as csv:
    txt = csv.read()

  linhas = [linha.strip() for linha in txt.splitlines()] #remover espaços
  txt = '\n'.join(linhas)
  
  txt = re.sub(r'"[^"]*[\n\r]+[^"]*"', lambda m: m.group(0).replace('\n', ' '), txt)

  return txt

def transforma_lista(lista):
  """função que transforma caracteres de números inteiros para o tipo int, 
  retirando espaços"""
  lista_transformada = []
  for item in lista:
    try:
      item = item.strip() #retira espaços antes e depois do texto
    except AttributeError:
      pass #se não for string, mantém como está
    try:
      item = int(item)
    except ValueError:
      pass #se não for inteiro, mantém como string
    lista_transformada.append(item)
  return lista_transformada
  
def pegar_primeiro_inteiro(x):
  "função que retorna s primeiro item da lista se forem inteiros como uma lista"
  for i in range(len(x)):
    if str(x[i]).isnumeric():
      return int(x[i])
      break

def pegar_condicao(x):
  cond = None
  if len(x) > 1:
    for i in range(len(x)-1, -1, -1): #retornar o item antes do último número inteiro
      try:
        int(x[i])
        cond = x[i-1]
        break
      except ValueError:
        pass
  return cond

def pegar_inteiro_cond(x):
  cond = None
  if len(x) > 1:
    for i in range(len(x)-1, -1, -1): #retornar o item antes do último número inteiro
      try:
        int(x[i])
        cond = int(x[i])
        break
      except ValueError:
        pass
  return cond

def xp ():
  #combate
  combate = pd.read_csv('docs_bronze/xp_combate.csv', encoding='utf-8')
  combate = combate.rename(columns={'Experiência':'XP'})
  combate['Profissao'] = "combate"
  combate = combate.rename(columns={'Monstro': 'item'})

  #cultivo
  cultivo = pd.read_csv('docs_bronze/xp_cultivo.csv', encoding='utf-8')
  cultivo['XP'] = cultivo['XP'].astype(int) #estava float
  cultivo = cultivo.rename(columns={'Cultivo': 'item', 'Estacao':'estacao_condicao'})

  #mineração
  mineracao = pd.read_csv('docs_bronze/xp_mineracao.csv', encoding='utf-8')
  #divide texto e lista de palavras
  mineracao.Experiências = mineracao.Experiências.apply(lambda x: x.split()) 
  mineracao['Experiências'] = mineracao.Experiências.apply(lambda lista: transforma_lista(lista))
  mineracao['XP'] = mineracao.Experiências.apply(lambda x: pegar_primeiro_inteiro(x))
  mineracao['estacao_condicao'] = mineracao.Experiências.apply(lambda x: pegar_condicao(x))
  mineracao['XP_condicional'] = mineracao.Experiências.apply(lambda x: pegar_inteiro_cond(x))
  mineracao.drop(columns=['Experiências'], inplace=True)
  mineracao['Profissao'] = 'mineracao'
  mineracao = mineracao.rename(columns={'Tipo de Rocha': 'item'})
  mineracao = mineracao[['Profissao','item','XP','estacao_condicao','XP_condicional']]

  #coleta
  coleta = pd.read_csv('docs_bronze/xp_coleta.csv', encoding='utf-8')
  coleta['XP'] = coleta.item.apply(lambda x: pegar_primeiro_inteiro(x))
  coleta.loc[6:12,'XP'] = 7
  coleta.XP = coleta.XP.astype(int)
  coleta.loc[0:3,'item'] = coleta.loc[0:3,'item'].apply(lambda linha: linha.split('por')[1])
  coleta.loc[5,'item'] = coleta.loc[5,'item'].split('para')[1]
  coleta.drop(4)
  coleta['Profissao'] = 'coleta'

  #pesca
  pesca = pd.read_csv('docs_bronze/xp_pesca.csv', encoding='utf-8') 
  pesca = pesca.rename(columns={'Total de Sardinhas (Sem estrelas)':'sardinhas',
                                'Total de Peixes Lendários com Estrela Dourada (Peixes com maior EXP)': 'lendarios',
                                'Total de Covos': 'covos'})
  df_pesca_melt = pd.melt(pesca, 
                          id_vars=['Experiência','Nível'],
                          value_vars=['sardinhas', 'lendarios', 'covos'], 
                          var_name='peixe', 
                          value_name='Quantidade')
  # Repetindo o valor de 'Experiência' para cada linha
  df_pesca_melt['XP'] = df_pesca_melt['Experiência'] / df_pesca_melt['Quantidade']
  df_pesca_melt['item'] = 'Nível ' + df_pesca_melt['Nível'].astype(str) + ' pescando ' + df_pesca_melt['peixe']
  df_pesca_melt['Profissao'] = 'pesca'

  pesca = df_pesca_melt[['Profissao','item','XP']]

  #concatenar no df xp
  lista_xp_dataframes = [combate,mineracao,coleta,pesca,cultivo]
  xp = pd.concat(lista_xp_dataframes)
  xp = xp[['item','XP','Profissao','estacao_condicao','XP_condicional']]
  xp.to_csv('docs_silver/xp.csv')

  pass

def limpar_preco(serie):
  """Limpa e converte uma série para float, tratando cada elemento individualmente.

  Args:
      serie: Uma Série do pandas.

  Returns:
      Uma nova Série com os valores limpos e convertidos para float (se possível).
  """

  def tratar_elemento(elemento):
      elemento = str(elemento).replace('ouros', '').replace('ouro', '').replace(' ', '').replace('g','')
      try:
          return float(elemento)
      except ValueError:
          return elemento

  return serie.apply(tratar_elemento)

def separar_e_explodir(df, coluna):
  """
    Separa as strings de uma coluna em novas linhas com base em letras maiúsculas
    e explode o resultado, evitando ValueError.

  Args:
      df: DataFrame Pandas.
      coluna: Nome da coluna a ser processada.

  Returns:
      DataFrame com as linhas explodidas.
  """

  # Função para separar as strings com base em letras maiúsculas
  def separar_por_maiusculas(texto):
      padrao_regex = r'\b[A-ZÁ-Ú][^A-ZÁ-Ú]*\b'
      return re.findall(padrao_regex, texto)

  # Aplicar a função e explodir, resetando o índice
  df[coluna] = df[coluna].apply(separar_por_maiusculas)
  df = df.explode(coluna)
  df = df.reset_index(drop=True)
  df[f'{coluna}_item'] = df[coluna].apply(lambda linha: linha.split('-')[0].strip())
  df[f'{coluna}_valor'] = df[coluna].apply(lambda linha: linha.split('-')[1].strip())
  df[f'{coluna}_valor'] = limpar_preco(df[f'{coluna}_valor'])
  df = df.drop(coluna, axis=1)
  return df

def separar_quantidades_e_explodir (df, coluna):
  df[coluna] = df[coluna].apply(lambda linha: linha.split(')'))
  df = df.explode(coluna).dropna(subset=coluna)
  #df = df.reset_index(drop=True)
  df[coluna] = df[coluna].apply(lambda linha: linha.split('(') if '(' in linha else [linha, '0'])
  df[f'{coluna}_item'] = df[coluna].apply(lambda lista: lista[0].strip())
  df[f'{coluna}_qtd'] = df[coluna].apply(lambda lista: lista[1].strip())
  df = df.drop(coluna, axis=1)
  df[f'{coluna}_qtd'] = pd.to_numeric(df[f'{coluna}_qtd'], errors='coerce')
  df = df[df[f'{coluna}_qtd'] != 0]

  return df

def tenta_dividir (texto_a_dividir, divisor: str = None,coluna: int = 0):
  """Função que divide colunas de valor, de saúde e de energia.
      args:
      texto_a_dividir: string qu eserá dividido em lista
      divisor: texto a ser aplicado no split
      coluna: índice da lista que vai retornar
  """
  texto_a_dividir = texto_a_dividir
  divisor = divisor
  coluna = coluna
  try:
    return texto_a_dividir.split(divisor)[coluna].strip()
  except IndexError:
    return texto_a_dividir
  except AttributeError:
    return texto_a_dividir

def divide_valores_por_qualidade (df, coluna_nome, coluna_valor, coluna_energia_saude):
  df = df
  coluna_nome = coluna_nome
  coluna_valor = coluna_valor
  coluna_energia_saude = coluna_energia_saude
  for i in range(0,len(df)):
    if i % 4 == 0:
      df.loc[i,coluna_valor] = tenta_dividir(texto_a_dividir=df.loc[i,coluna_valor],divisor='ouros',coluna=0)
      df.loc[i,'Energia'] = tenta_dividir(texto_a_dividir=df.loc[i,coluna_energia_saude],coluna=0)
      df.loc[i,'Saude'] = tenta_dividir(texto_a_dividir=df.loc[i,coluna_energia_saude],coluna=1)
    if i % 4 == 1:
      df.loc[i,coluna_nome] = df.loc[i,coluna_nome] + '_prata'
      df.loc[i,coluna_valor] = tenta_dividir(texto_a_dividir=df.loc[i,coluna_valor],divisor='ouros',coluna=1)
      df.loc[i,'Energia'] = tenta_dividir(texto_a_dividir=df.loc[i,coluna_energia_saude],coluna=2)
      df.loc[i,'Saude'] = tenta_dividir(texto_a_dividir=df.loc[i,coluna_energia_saude],coluna=3)
    if i % 4 == 2:
      df.loc[i,coluna_nome] = df.loc[i,coluna_nome] + '_ouro'
      df.loc[i,coluna_valor] = tenta_dividir(texto_a_dividir=df.loc[i,coluna_valor],divisor='ouros',coluna=2)
      df.loc[i,'Energia'] = tenta_dividir(texto_a_dividir=df.loc[i,coluna_energia_saude],coluna=4)
      df.loc[i,'Saude'] = tenta_dividir(texto_a_dividir=df.loc[i,coluna_energia_saude],coluna=5)
    if i % 4 == 3:
      df.loc[i,coluna_nome] = df.loc[i,coluna_nome] + '_iridio'
      df.loc[i,coluna_valor] = tenta_dividir(texto_a_dividir=df.loc[i,coluna_valor],divisor='ouros',coluna=3)
      df.loc[i,'Energia'] = tenta_dividir(texto_a_dividir=df.loc[i,coluna_energia_saude],coluna=6)
      df.loc[i,'Saude'] = tenta_dividir(texto_a_dividir=df.loc[i,coluna_energia_saude],coluna=7)
  return df

def concat_dataframes ():
  
  #animais
  lista_animais = ['avestruz',
                   'cabra',
                   'coelho',
                   'dinossauro',
                   'galinha',
                   'ovelha',
                   'pato',
                   'porco',
                   'vaca']
  colunas_inicial=['',
                   'Imagem',
                  'Nome',
                  'Custo',
                  'Requisitos',
                  'Produz',
                  'Preço de venda com 5 corações']
  colunas_renomeado=['col0',
                    'Imagem',
                    'Nome',
                    'Custo',
                    'Requisitos',
                    'Produz',
                    'Venda_5_coracoes']  
  rename_dict = dict(zip(colunas_inicial, colunas_renomeado))
  dfs_to_concat = []
  for animal in lista_animais:
    df_temp = pd.read_csv(f'docs_bronze/animais_{animal}.csv')
    df_temp = df_temp.rename(columns=rename_dict)
    dfs_to_concat.append(df_temp)
  df_animais = pd.concat(dfs_to_concat, ignore_index=True).reset_index(drop=True)
  df_animais['Custo'] = limpar_preco(df_animais['Custo'])
  df_animais['Venda_5_coracoes'] = limpar_preco(df_animais['Venda_5_coracoes'])
  df_animais['Produz'] = df_animais['Produz'].apply(lambda linha: linha.replace('Avestruz','avestruz').replace('Dourado','dourado'))
  df_animais = separar_e_explodir(df_animais,'Produz')
  df_animais = df_animais[['Nome','Custo','Requisitos','Produz_item','Produz_valor','Venda_5_coracoes']]  
  df_animais.to_csv('docs_silver/animais.csv', encoding='utf-8')

  #armas
  lista_armas = ['adagas',
                'clavas',
                'espadas',
                'estilingues',
                'impossiveis',
                'municoes']
  dfs_to_concat = [] 
  for arma in lista_armas:
    df_temp = pd.read_csv(f'docs_bronze/armas_{arma}.csv')
    df_temp['Tipo'] = arma
    if arma == 'municoes':
      df_temp = df_temp.rename(columns={'Faixa de Dano Padrão': 'Dano', 
                                        'Item': 'Nome',
                                        'Chance de  Acerto Crítico': 'Chance de Acerto Crítico'})
      df_temp['Descrição'] = df_temp['Multiplicador de Munição'].apply(lambda x: 'Base de dano: ' + str(x))
      df_temp['Nome'] = df_temp['Nome'].apply(lambda linha: str(linha.replace('Todas as  ','').replace('  • Todos os ',', ').replace('"','')))
      df_temp.pop('Multiplicador de Munição')
    if arma == 'impossiveis':
      df_temp = df_temp.rename(columns={'Preço de venda':'Preço de Venda'})
    
    dfs_to_concat.append(df_temp)
  df_armas = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  df_armas['Preço de Compra'] = limpar_preco(df_armas['Preço de Compra'])
  df_armas['Preço de Venda'] = limpar_preco(df_armas['Preço de Venda'])
  df_armas = df_armas.drop(columns=['Unnamed: 0','Imagem'])
  df_armas = df_armas[['Nome','Tipo','Nível','Descrição','Dano','Chance de Acerto Crítico','Estatísticas','Localização','Preço de Compra','Preço de Venda','Chance de  Acerto Crítico']]
  df_armas.to_csv('docs_silver/armas.csv', encoding='utf-8')


  #atributos luta
  df_atributos_luta = pd.read_csv('docs_bronze/armas_luta_atributos.csv',encoding='utf-8')
  df_atributos_luta = df_atributos_luta.drop(['Unnamed: 0','Imagem'], axis=1)
  df_atributos_luta.to_csv('docs_silver/atributos_luta.csv', encoding='utf-8')

  
  #artefatos
  artefato_tesouro = pd.read_csv('docs_bronze/artefatos_tesouro.csv')
  artefato_tesouro.columns = ['','Imagem','Nome','Descrição','Local']
  artefatos = pd.read_csv('docs_bronze/artefatos.csv')
  lista_artefatos = [artefatos,artefato_tesouro]
  artefatos = pd.concat(lista_artefatos,join='outer',ignore_index=True)
  artefatos = artefatos.drop(columns='')
  artefatos['Preço'] = limpar_preco(artefatos['Preço'])
  artefatos.to_csv('docs_silver/artefatos.csv',encoding='utf-8')

  
  #artesanato
  lista_produtos = ['aneis',
                    'aspersores',
                    'bombas',
                    'cercas',
                    'decoracao',
                    'diversos',
                    'equipamento_refino',
                    'equipamentos_artesanais',
                    'fertilizantes',
                    'iluminacao',
                    'itens_comestiveis',
                    'mobilia',
                    'pesca',
                    'sementes']
  dfs_to_concat = [] 
  for artesanato in lista_produtos:
    df_temp = pd.read_csv(f'docs_bronze/artesanato_{artesanato}.csv')
    df_temp['Tipo'] = artesanato
    dfs_to_concat.append(df_temp)
  df_artesanatos = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  df_artesanatos = df_artesanatos.drop(columns=['Unnamed: 0','Imagem'])
  df_artesanatos = separar_quantidades_e_explodir(df_artesanatos,'Ingredientes')
  df_artesanatos = df_artesanatos[['Nome','Descrição','Tipo','Ingredientes_item','Ingredientes_qtd','Fonte da Receita','Origem da Receita','Dura Por','Energia','Saúde']]
  df_artesanatos.to_csv('docs_silver/produtos.csv', encoding='utf-8')

  
  #arvores
  lista_arvores: list = ['bananeira',
                         'cerejeira',
                         'damasqueiro',
                         'laranjeira',
                         'macieira',
                         'mangueira',
                         'pessegueira',
                         'romanzeira']
  dfs_to_concat = [] 
  for arvore in lista_arvores:
    serie_arvore = pd.read_csv(f'docs_bronze/arvores_{arvore}.csv').iloc[1,1:]
    serie_arvore['Unnamed: 0'] = 0
    serie_muda = pd.read_csv(f'docs_bronze/arvores_muda_{arvore}.csv').iloc[0,1:]
    serie_final = serie_muda._append(serie_arvore)
    df_final = pd.DataFrame(serie_final).T.reset_index(drop=True)
    dfs_to_concat.append(df_final)
  df_arvores = pd.concat([df.reset_index(drop=True) for df in dfs_to_concat]*4,
                         ignore_index=True).sort_values(by='Fruta')
  df_arvores = df_arvores.reset_index(drop=True)
  df_arvores = divide_valores_por_qualidade(df = df_arvores,
                                            coluna_nome = 'Fruta',
                                            coluna_valor = 'Preço de venda',
                                            coluna_energia_saude = 'Efeito de Cura')  
  df_arvores = df_arvores.rename(columns = {'Preço da Muda': 'preco_muda_pierre',
                                          'Preço da Muda.1': 'preco_muda_carrinho_viagem',
                                          'Preço de venda': 'Preco_venda'})
  df_arvores = df_arvores[['Fruta',
                           'Muda',
                           'Preco_venda',
                           'Energia',
                           'Saude',
                           'Vendido por',
                           'Usado em',
                           'Estágio 1',
                           'Estágio 2',
                           'Estágio 3',
                           'Estágio 4',
                           'Estágio 5 - Primavera, Verão, Outono, Inverno',
                           'Colheita',
                           'preco_muda_pierre',
                           'preco_muda_carrinho_viagem']]
  df_arvores.to_csv('docs_silver/arvores.csv', encoding='utf-8', index=False)


  
  #vestuario
  lista_vestuario = ['aneis',
                     'calcados',
                     'chapeus']
  dfs_to_concat = [] 
  for vestuario in lista_vestuario:
    df_temp = pd.read_csv(f'docs_bronze/{vestuario}.csv', index_col='Unnamed: 0')
    df_temp['Tipo'] = vestuario
    dfs_to_concat.append(df_temp)
  df_vestuarios = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  print(df_vestuarios.columns)
  df_vestuarios = df_vestuarios[['Nome','Tipo','Descrição','Efeito','Localização','Ingredientes','Preço de Compra','Preço de Venda','Estatísticas','Conquista','Como obter']]
  #df_vestuarios = separar_quantidades_e_explodir(df_vestuarios,'Ingredientes')
  df_vestuarios.to_csv('docs_silver/vestuarios.csv', encoding='utf-8')

  #calendario
  lista_datas = ['primavera_aniversario',
                 'primavera_festivais',
                 'verao_aniversario',
                 'verao_festivais',
                 'outono_aniversario',
                 'outono_festivais',
                 'inverno_aniversario',
                 'inverno_festivais']
  dfs_to_concat = []
  i = 1
  for data in lista_datas:
    df_temp = pd.read_csv(f'docs_bronze/calendario_{data}.csv')
    df_temp['Mes'] = str(i//2) + '.' + data.split('_')[0]
    df_temp['Evento'] = data.split('_')[1]
    df_temp = df_temp.rename(columns={'Aldeões':'Nome','Aldeão':'Nome'})
    dfs_to_concat.append(df_temp)    
    i += 0.5
  df_calendario = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  df_calendario = df_calendario[['Dia','Mes','Evento','Nome']]
  df_calendario.to_csv('docs_silver/calendario.csv', encoding='utf-8')

  #calendário cultivos

  #carteira
  carteira_especiais = pd.read_csv(f'docs_bronze\carteira_itens_especiais.csv')
  carteira_livros = pd.read_csv(f'docs_bronze\carteira_livros_poderes_especiais.csv')
  carteira_poderes = pd.read_csv(f'docs_bronze\carteira_poderes_maestria.csv')
  df_carteira = pd.concat([carteira_especiais,carteira_livros,carteira_poderes],ignore_index=True).reset_index(drop=True)
  df_carteira = df_carteira[['Nome','Uso','Obtenção','Descrição','Localização']]  
  df_carteira.to_csv('docs_silver/carteira.csv', encoding='utf-8')

  #caverna
  caverna_cogumelo = pd.read_csv(f'docs_bronze\caverna_cogumelo.csv')
  caverna_morcego = pd.read_csv(f'docs_bronze\caverna_morcego.csv')
  caverna_morcego = caverna_morcego.rename(columns={'Renda':'Lucro'})
  df_caverna = pd.concat([caverna_cogumelo,caverna_morcego]*4,ignore_index=True).reset_index(drop=True).sort_values(by='Nome')
  df_caverna = df_caverna.dropna(subset=['Descrição'],ignore_index=True) #apaga linhas onde Descrição está vazio
  df_caverna = divide_valores_por_qualidade(df = df_caverna,
                                            coluna_nome= 'Nome',
                                            coluna_valor= 'Lucro',
                                            coluna_energia_saude = 'Recupera')
  
  df_caverna = df_caverna[['Nome','Lucro','Energia','Saude','Usado em','Chance','Descrição','Também achado']]
  df_caverna.to_csv('docs_silver/caverna.csv', encoding='utf-8')

  #clima
  df_clima = pd.read_csv('docs_bronze\clima.csv', encoding='utf-8')
  df_clima = df_clima[['Clima','Descrição']]
  df_clima.to_csv('docs_silver/clima.csv', encoding='utf-8')

  #coleta  
  lista_coleta = ['cavernas',
                 'deserto',
                 'ilha_gengibre',
                 'inverno',
                 'outono',
                 'praia',
                 'primavera',
                 'seiva',
                 'verao']
  #padronizar colunas
  dfs_to_concat = [] 
  for coleta in lista_coleta:
    df_temp = pd.read_csv(f'docs_bronze/coleta_{coleta}.csv')
    df_temp =df_temp.rename(columns={'Usado Em':'Usado em', 'Encontrado':'Encontrado em'})
    dfs_to_concat.append(df_temp)
  df_coleta = pd.concat(dfs_to_concat*4,ignore_index=True)
  df_coleta = df_coleta.sort_values(by='Nome').reset_index(drop=True)
  df_coleta = divide_valores_por_qualidade(df = df_coleta, 
                                           coluna_nome = 'Nome', 
                                           coluna_valor = 'Lucro', 
                                           coluna_energia_saude = 'Efeito')
  df_coleta = df_coleta[['Nome','Lucro','Energia','Saude','Usado em','origem','Encontrado em','Descrição']]
  df_coleta = df_coleta.drop(index=[49,50,51,157,158,159]).dropna(subset=['Descrição'],ignore_index=True).reset_index(drop=True)
  df_coleta.to_csv('docs_silver/coleta.csv', encoding='utf-8')

  #conjunto
  lista_conjunto = ['2500',
                 '5000',
                 '10000',
                 '25000',
                 'a_desaparecida',
                 'animal',
                 'artesao',
                 'aventureiro',
                 'construcao',
                 'cozinheiro',
                 'encantador',
                 'ferreiro',
                 'forragem',
                 'geologo',
                 'inverno',
                 'outono',
                 'peixes_especializados',
                 'peixes_lago',
                 'peixes_oceano',
                 'peixes_rio',
                 'pesca_covo']
  #padronizar colunas
  dfs_to_concat = []
  for conjunto in lista_conjunto:
    df_temp = pd.read_csv(f'docs_bronze/conjunto_{conjunto}.csv')
    #transformar linha Recompensa: em coluna
    df_temp['Recompensa'] = df_temp.iloc[-1,2]
    #Repetir nome da coluna na primeira coluna
    df_temp.iloc[:,0] = df_temp.columns[0]
    if conjunto == 'a_desaparecida':
      df_temp.iloc[7,]
    #Mudar o nome das Colunas para ['Conjunto','Requisitos','Descrição_requisitos','Recompensa']
    print(df_temp.columns)
    df_temp.columns = ['Conjunto','Requisitos','Descrição_requisitos','Recompensa']
    
    dfs_to_concat.append(df_temp)
  df_conjuntos = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  df_conjuntos.to_csv('docs_silver/conjuntos.csv', encoding='utf-8')

  #culinaria
  lista_culinaria = ['covo',
                    'cultivos',
                    'diversos',
                    'frutas_arvore',
                    'itens_coleta',
                    'itens_loja',
                    'mercadorias_artesanais',
                    'pescaria',
                    'pratos_ingredientes',
                    'produtos_naturais',
                    'receitas']
  #padronizar colunas
  dfs_to_concat = [] 
  for culinaria in lista_culinaria:
    df_temp = pd.read_csv(f'docs_bronze/culinaria_{culinaria}.csv')
    #print(f'colunas de {culinaria}: {df_temp.columns}')
    dfs_to_concat.append(df_temp)
  df_culinaria = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  df_culinaria.to_csv('docs_silver/culinaria.csv', encoding='utf-8')

  #custo_solo
  solo_concha = pd.read_csv(f'docs_bronze\custo_solo_foliar_concha.csv', header=0)
  solo_coral = pd.read_csv(f'docs_bronze\custo_solo_foliar_coral.csv', header=0)
  df_solo = pd.concat([solo_concha,solo_coral],ignore_index=True).reset_index(drop=True)
  df_solo.to_csv('docs_silver/solo_foliar.csv', encoding='utf-8')  

  #casa/estufa
  lista_casa = ['casa_estagios',
                      'casa_renovacoes',
                      'estufa']
  #padronizar colunas
  dfs_to_concat = [] 
  for casa in lista_casa:
    df_temp = pd.read_csv(f'docs_bronze/{casa}.csv')
    print(f'colunas de {casa}: {df_temp.columns}')
    dfs_to_concat.append(df_temp)
  df_casa = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  df_casa.to_csv('docs_silver/casa.csv', encoding='utf-8')

  #ferramenta
  lista_ferramentas = ['enxada',
                      'lixeira',
                      'machado',
                      'picareta',
                      'regador',
                      'vara_pesca']
  #padronizar colunas
  dfs_to_concat = [] 
  for ferramenta in lista_ferramentas:
    df_temp = pd.read_csv(f'docs_bronze/ferramenta_{ferramenta}.csv')
    print(f'colunas de {ferramenta}: {df_temp.columns}')
    dfs_to_concat.append(df_temp)
  df_ferramentas = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  df_ferramentas.to_csv('docs_silver/ferramentas.csv', encoding='utf-8')

  #iscas
  df_iscas = pd.read_csv('docs_bronze\iscas.csv', encoding='utf-8')
  df_iscas.to_csv('docs_silver/iscas.csv', encoding='utf-8')

  #lavoura
  lista_lavouras = ['broto_cha',
                    'grao_cafe',
                    'muda_feijao',
                    'muda_lupulo',
                    'muda_uva',
                    'semente_abacaxi',
                    'semente_abobora',
                    'semente_alcachofra',
                    'semente_alho',
                    'semente_amaranto',
                    'semente_antiga',
                    'semente_arroz',
                    'semente_batata',
                    'semente_berinjela',
                    'semente_beterraba',
                    'semente_cacto',
                    'semente_carambola',
                    'semente_cenoura',
                    'semente_chirivia',
                    'semente_cuove_chinesa',
                    'semente_couve_flor',
                    'semente_couve',
                    'semente_fada',
                    'semente_girassol',
                    'semente_inhame',
                    'semente_jasmin_azul',
                    'semente_melao',
                    'semente_micanga',
                    'semente_milho',
                    'semente_mirtilo',
                    'semente_morango',
                    'semente_oxicoco',
                    'semente_papoula',
                    'semente_pimenta',
                    'semente_rabanete',
                    'semente_rara',
                    'semente_repolho',
                    'semente_rubiarmo',
                    'semente_tomate',
                    'semente_trigo',
                    'semente_tulipa']
  #padronizar colunas
  dfs_to_concat = [] 
  for lavoura in lista_lavouras:
    df_temp = pd.read_csv(f'docs_bronze/lavoura_{ferramenta}.csv')
    print(f'colunas de {lavoura}: {df_temp.columns}')
    dfs_to_concat.append(df_temp)
  df_lavouras = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  df_lavouras.to_csv('docs_silver/lavouras.csv', encoding='utf-8')

  #lista_presente
  df_presentes = pd.read_csv('docs_bronze\lista_presentes.csv', encoding='utf-8')
  df_presentes.to_csv('docs_silver/lista_presentes.csv', encoding='utf-8')

  #mercadoria
  lista_maquinas = ['apiario',
                    'barril_madeira',
                    'barril',
                    'gerador_oleo',
                    'jarra_conserva',
                    'maquina_molho',
                    'prensa_queijo',
                    'maquina_maionese',
                    'tear']
  #padronizar colunas
  dfs_to_concat = [] 
  for maquina in lista_maquinas:
    df_temp = pd.read_csv(f'docs_bronze/mercadoria_{maquina}.csv')
    print(f'colunas de {maquina}: {df_temp.columns}')
    dfs_to_concat.append(df_temp)
  df_maquina = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  df_maquina.to_csv('docs_silver/maquinas.csv', encoding='utf-8')


  #produtos
  lista_mercadorias = ['mel',
                      'produto_barril_madeira',
                      'produto_barril',
                      'produto_gerador_oleo',
                      'produto_jarra_conserva',
                      'produto_maquina_molho',
                      'produto_prensa_queijo',
                      'produto_maquina_maionese',
                      'produto_tear']
  #padronizar colunas
  dfs_to_concat = [] 
  for mercadoria in lista_mercadorias:
    df_temp = pd.read_csv(f'docs_bronze/mercadoria_{mercadoria}.csv')
    print(f'colunas de {mercadoria}: {df_temp.columns}')
    dfs_to_concat.append(df_temp)
  df_mercadorias = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  df_mercadorias.to_csv('docs_silver/mercadorias.csv', encoding='utf-8')

  #minerais
  lista_minerais = ['coleta',
                    'gemas',
                    'geodos',
                    'origem_geodos']
  #padronizar colunas
  dfs_to_concat = [] 
  for mineral in lista_minerais:
    df_temp = pd.read_csv(f'docs_bronze/mineral_{mercadoria}.csv')
    print(f'colunas de {mineral}: {df_temp.columns}')
    dfs_to_concat.append(df_temp)
  df_minerais = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  df_minerais.to_csv('docs_silver/minerais.csv', encoding='utf-8')

  #missao
  lista_missoes = ['_especiais_sr_qi',
                    '_itens_lista',
                    '_lista',
                    '_pedidos_especiais',
                    '']
  #padronizar colunas
  dfs_to_concat = [] 
  for missao in lista_missoes:
    df_temp = pd.read_csv(f'docs_bronze/missao{missao}.csv')
    print(f'colunas de {missao}: {df_temp.columns}')
    dfs_to_concat.append(df_temp)
  df_missoes = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  df_missoes.to_csv('docs_silver/missoes.csv', encoding='utf-8')

  #mobilia
  lista_mobilias = ['aquarios',
                    'bancos',
                    'bandeiras',
                    'cadeiras1',
                    'cadeiras2',
                    'cadeiras3',
                    'camas',
                    'catalogo',
                    'comodas',
                    'decoracao_parede',
                    'diversos1',
                    'diversos2',
                    'estantes',
                    'itens_especiais1'
                    'itens_especiais2'
                    'janelas',
                    'lampadas',
                    'lareiras',
                    'mesas_longas',
                    'mesas1',
                    'mesas2',
                    'mesas3',
                    'outras_decoracoes1',
                    'outras_decoracoes2',
                    'pinturas_mercado_noturno',
                    'pinturas',
                    'plantas_decorativas_chao1',
                    'plantas_decorativas_chao2',
                    'plantas_decorativas_penduradas',
                    'poltronas',
                    'posteres',
                    'sofas',
                    'tapetes',
                    'tochas',
                    'tvs']
  #padronizar colunas
  dfs_to_concat = [] 
  for mobilia in lista_mobilias:
    df_temp = pd.read_csv(f'docs_bronze/mobilia_{mobilia}.csv')
    print(f'colunas de {mobilia}: {df_temp.columns}')
    dfs_to_concat.append(df_temp)
  df_mobilias = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  df_mobilias.to_csv('docs_silver/mobilias.csv', encoding='utf-8')

  #nos_minerio
  df_minerios_nos = pd.read_csv(f'docs_bronze/nos_minerio.csv')
  df_minerios_nos.to_csv('docs_silver/minerios_nos.csv', encoding='utf-8')

  #peixes
  lista_peixes = ['covo',
                    'itens_pescaveis',
                    'lendarios',
                    'lendarios_ii',
                    'mercado_noturno',
                    'receitas_pesca']
  #padronizar colunas
  dfs_to_concat = [] 
  for peixe in lista_peixes:
    df_temp = pd.read_csv(f'docs_bronze/peixes_{peixe}.csv')
    print(f'colunas de {peixe}: {df_temp.columns}')
    dfs_to_concat.append(df_temp)
  df_peixes = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  df_peixes.to_csv('docs_silver/peixes.csv', encoding='utf-8')

  #pesca
  lista_pescas = ['bau',
                  'comida',
                  'varas_pesca',
                  'zona']
  #padronizar colunas
  dfs_to_concat = [] 
  for pesca in lista_pescas:
    df_temp = pd.read_csv(f'docs_bronze/pesca_{pesca}.csv')
    print(f'colunas de {pesca}: {df_temp.columns}')
    dfs_to_concat.append(df_temp)
  df_pescas = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  df_pescas.to_csv('docs_silver/pescas.csv', encoding='utf-8')

  #solos_producao
  df_solos_producao = pd.read_csv('docs_bronze\solos_producao.csv', encoding='utf-8')
  # transformar colunas
  df_solos_producao.to_csv('docs_silver\solos_producao.csv', encoding='utf-8')
  
  #taxa_cultivo
  lista_taxas_cultivo = ['fertilizante_qualidade',
                        'fertilizante_basico',
                        'fertilizante_premium',
                        'solo_normal']
  #padronizar colunas
  dfs_to_concat = [] 
  for taxa in lista_taxas_cultivo:
    df_temp = pd.read_csv(f'docs_bronze/taxa_cultivo_{taxa}.csv')
    print(f'colunas de {taxa}: {df_temp.columns}')
    dfs_to_concat.append(df_temp)
  df_taxas_cultivo = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  df_taxas_cultivo.to_csv('docs_silver/taxas_cultivo.csv', encoding='utf-8')

  
  pass




if __name__ == '__main__':
  import pandas as pd
  import re
  profissoes()
  limpar_csv('docs_bronze/xp_coleta.csv')
  xp()
  concat_dataframes()


"""
def fertilizante ():
  for i in ['Normal','Fertilizante Básico','Fertilizante de Qualidade']:
    grafico = sns.barplot(data=df_solos[df_solos['Melhoramento']==i],
                x='nivel_habilidade_cultivo',
                y='percentual',
                hue='qualidade_produto',
                estimator='sum',
                #dodge=False,
                errorbar=None)
    grafico.set_title(f'Qualidade do cultivo: {i}')
    grafico.set_xlabel('Nível de habilidade Cultivo')
    grafico.set_ylabel('Percentual')
    #tamanho do gráfico
    grafico.figure.set_size_inches(10, 5)
    plt.show()

  #coleta
  #listar variaveis do código do tipo dataframe
  variaveis = dir()
  qtd_variaveis = 0
  variavel_dataframe = ['selecione um dataframe']
  #print(f'todas variáveis: {variaveis}')
  for variavel in variaveis:
      if (type(eval(variavel)) == pd.core.frame.DataFrame and not variavel.startswith('_')):
          #print(variavel)
          variavel_dataframe.append(eval(variavel))
          qtd_variaveis += 1

  print(f'Quantidade de variáveis: {qtd_variaveis}')

#criar um menu seletor de dataframe a partir de variavel_dataframe para mostrar

# initial_value = variavel_dataframe[0]  # Or another valid value

menu = widgets.Dropdown(options=variavel_dataframe)

menu.observe(visualiza)
display(menu)










def processar_dataframe(df):
    
    #Processa um DataFrame, separando as informações nas colunas 'Efeito' e 'Lucro'
    #e criando novas colunas com base nas qualidades especificadas.

    #Args:
    #    df (pd.DataFrame): O DataFrame a ser processado.
   # 


    #imprimir nome do dataframe
    for name, value in globals().items():
        if value is df:
            print(f'iniciar {name}')

     # Separar texto das colunas em itens de lista e transformar em inteiro
    try: #alguns dataframes não tem efeito
      df['Efeito'] = df['Efeito'].apply(lambda x: x.split())
      df['Lucro'] = df['Lucro'].apply(lambda x: x.split())
    except KeyError:
      pass
    except AttributeError:
      pass


    qualidades = ['prata', 'ouro', 'iridio']
    colunas_efeito = [[2, 3], [4, 5], [6, 7]]
    colunas_lucro = [2, 4, 6]

    dfs = []
    for i, qualidade in enumerate(qualidades):
        df_temp = df.copy()
        df_temp['Qualidade'] = qualidade
        for linha in df_temp.index:
            try:
              if len(df_temp.loc[linha,'Lucro']) > 2:
                df_temp.loc[linha, 'Lucro'] = df_temp.loc[linha, 'Lucro'][colunas_lucro[i]]
                try: #há dataframes sem Efeito
                  df_temp.loc[linha, 'Energia'] = df_temp.loc[linha, 'Efeito'][colunas_efeito[i][0]]
                  df_temp.loc[linha, 'Saude'] = df_temp.loc[linha, 'Efeito'][colunas_efeito[i][1]]
                except KeyError:
                  pass
                except IndexError:
                  pass
            except TypeError:
              pass
            except AttributeError:
              pass
        dfs.append(df_temp)

    # Tratar dado de normal separadamente
    df_temp = df.copy()
    df_temp['Qualidade'] = 'normal'

    for linha in df_temp.index:
      try:
        df_temp.loc[linha, 'Energia'] = df_temp.loc[linha, 'Efeito'][0]
        df_temp.loc[linha, 'Saude'] = df_temp.loc[linha, 'Efeito'][1]
        df_temp.drop(columns=['Efeito'], inplace=True)
      except KeyError:
        df_temp.loc[linha, 'Energia'] = 0
        df_temp.loc[linha, 'Saude'] = 0
      try:
        df_temp.loc[linha, 'Lucro'] = df_temp.loc[linha, 'Lucro'][0]
      except TypeError:
        pass
    dfs.append(df_temp)

    #imprimir nome do dataframe
    for name, value in globals().items():
        if value is df:
            print(f'df {name} finalizado com sucesso')

    # Concatenar e remover coluna 'Efeito'
    df = pd.concat(dfs)

    return df

dfs_coleta = [seiva_coleta, primavera_coleta, verao_coleta, outono_coleta,
              inverno_coleta, praia_coleta, cavernas_coleta,
              deserto_coleta, ilha_gengibre_coleta]

for i, df in enumerate(dfs_coleta):
    dfs_coleta[i] = processar_dataframe(df)

# concatenar dataframes da lista dfs_coleta
dfs_coleta = pd.concat(dfs_coleta,ignore_index=True)

#apagar dataframes originais da memória
del seiva_coleta
del primavera_coleta
del verao_coleta
del outono_coleta
del inverno_coleta
del praia_coleta
del cavernas_coleta
del deserto_coleta
del ilha_gengibre_coleta

dfs_coleta
#se funcionar, substituirá a célula abaixo


    # retira número inteiro na coluna item para colocar na coluna XP
    def extrair_numero(x):
        try:
            return int(x.split()[0])
        except ValueError:
            return None

    xp_coleta['XP'] = xp_coleta.item.apply(lambda x: extrair_numero(x))
    xp_coleta.iloc[6:13,1] = 7


"""

