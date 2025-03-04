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

def extrair_valor_moeda(preco):
  """
  Extrai o valor e a moeda de uma coluna de preço, caso não seja float
  Args:
      preco: Uma string com o preço.
  Returns:
      Uma tupla com o valor e a moeda.
      Ex: ('100', 'ouros')
          ('5', 'Bananas')

  """
  try:
    match = re.match(r'(\d+)\s*(\w+)', preco)  
    if match:
        return match.group(1), match.group(2)
    match = re.match(r'(\w+)\s*\((\d+)\)', preco)
    if match:
        return match.group(2), match.group(1)
    return None, None
  except TypeError:
    return preco, None


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

  def tratar_elemento(elemento, coluna:int = 0):
      """
      Trata um elemento individualmente retirando o nome 'ouros', 'ouro' ou 'g'
      para retornar apenas o valor numérico.
      
      Args:
          elemento: Um elemento da Série.
          coluna: índice da lista que vai retornar
      
      Returns:
          Um valor numérico.
      """
      elemento = str(elemento).replace('ouros', '').replace('ouro', '').replace(' ', '').replace('g','')
      try:
          return float(elemento)[coluna]
      except ValueError:
          return elemento
      except TypeError:
          return float(elemento)

  return serie.apply(tratar_elemento)

def precos_carrinho_viagem(elemento: str, 
                           separador: str = '–', 
                           minimo: bool = False, 
                           maximo: bool = False):
  """Calcula o preço médio, mínimo e máximo de uma string que representa uma faixa de preço separado por '-'.

  Args:
      elemento: Um elemento de preço.

  Returns:
      Uma tupla com o preço médio, mínimo e máximo do elemento.
  """
  
  if isinstance(elemento, float):
    return elemento
  else:
    elemento = str(elemento).replace(' ', '').replace(' ', '')
    partes = elemento.split(separador)
    if len(partes) == 2:
      valor_minimo = float(partes[0])
      valor_maximo = float(partes[1])
      if minimo:  
        return valor_minimo
      if maximo:
        return valor_maximo

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

def dano_medio(linha):
  try:
    partes = linha.split('-')
    if len(partes) == 2:
      resultado = (int(partes[0]) + int(partes[1])) / 2
      return resultado
    else:
      return None
  except ValueError:
    return None
  except IndexError:
    return None

def tenta_separar_string (linha: str, divisor):
  """
    Tenta separar as strings de um texto
    em lista.

  Args:
      linha (str): Célula de um dataframe.
      divisor (str ou list): String ou lista de strings 
      que serão utilizados para dividir o string.

  Returns:
      Texto transformado em lista de itens dividida.
  """
  texto_dividido = []
  if not isinstance(linha, str):
    texto_dividido = linha
  elif not isinstance(divisor, list):
    divisor = [divisor]
    for cada_divisor in divisor:
      if cada_divisor in linha:
          partes = linha.split(cada_divisor)
          for parte in partes:
              parte = parte.strip()
              texto_dividido.append(parte)
  return texto_dividido
  
def separar_dias(valor):
  import ast
  """
    Separa as strings de um valor em novas linhas com base em separadores de datas.

    Args: 
      valor: string a ser processada.

    Returns:
      Lista com as datas separadas.
  """
  if '-' in str(valor):#por intervalo de datas com '-'
    partes = valor.split('-')
    lista = list(range(int(partes[0]),int(partes[1])+1)) #adiciona intermediários
  elif ',' in str(valor):  #lista de datas com ','
    lista = str(valor).replace(',', '').replace('e','').split(' ')
    lista = list(filter(None, lista))
  else:
    lista = valor
  return lista

def separar_quantidades_e_explodir (df, coluna, divisor: str = ')'):
  """
    Separa as strings de uma coluna em novas linhas com base 
    em lista de itens e quantidades.

  Args:
      df: DataFrame Pandas.
      coluna: Nome da coluna a ser processada.

  Returns:
      DataFrame com as linhas explodidas.
  """
  df[coluna] = df[coluna].apply(lambda linha: tenta_separar_string(linha=linha,divisor=divisor)) #separa itens
  df = df.explode(coluna).dropna(subset=coluna)
  df[coluna] = df[coluna].apply(lambda linha: linha.split('(') if '(' in linha else [linha, '0']) #separa qunatidades
  df[f'{coluna}_item'] = df[coluna].apply(lambda lista: lista[0].strip())
  df[f'{coluna}_qtd'] = df[coluna].apply(lambda lista: lista[1].strip())
  df = df.drop(coluna, axis=1)
  df[f'{coluna}_qtd'] = pd.to_numeric(df[f'{coluna}_qtd'], errors='coerce')
  df = df[df[f'{coluna}_qtd'] != 0]

  return df

def tenta_dividir (texto_a_dividir, divisor: str = None,coluna: int = 0):
  """Função que divide colunas de requisitos.
      Args:
      texto_a_dividir: string que será dividido em lista
      divisor: texto a ser aplicado no split
      coluna: índice da lista que vai retornar

      Returns:
      texto_a_dividir ou texto dividido em lista
  """
  
  try:
    return texto_a_dividir.split(divisor)[coluna].strip()
  except IndexError:
    return texto_a_dividir
  except AttributeError:
    return texto_a_dividir
  except ValueError:
    return texto_a_dividir

def divide_valores_por_qualidade (df, coluna_nome, coluna_valor, coluna_energia_saude = None):
  """
  Função que divide dataframe quadruplicado para qualidficar separadamente 
  as 4 qualidades: normal, prata, ouro e irídio.

  Args:
      df: DataFrame Pandas.
      coluna_nome: Nome da coluna onde os nome a serão substituídos por, incluindo as qualidades.
      coluna_valor: Nome da coluna de valor em ouros (4 valores) para ser dividido nas 4 qualidades.
      coluna_energia_saude (opcional): Nome da coluna com 8 valores a ser dividido nas 4 qualidades.
  
  Returns: df com as colunas divididas em 4 qualidades + 2 colunas 'Energia' e 'Saude'.
  """
  for i in range(0,len(df)):
    if i % 4 == 0:
      df.loc[i,coluna_valor] = tenta_dividir(texto_a_dividir=df.loc[i,coluna_valor],divisor='ouros',coluna=0)
      if coluna_energia_saude:
        df.loc[i,'Energia'] = tenta_dividir(texto_a_dividir=df.loc[i,coluna_energia_saude],coluna=0)
        df.loc[i,'Saude'] = tenta_dividir(texto_a_dividir=df.loc[i,coluna_energia_saude],coluna=1)
    if i % 4 == 1:
      df.loc[i,coluna_nome] = df.loc[i,coluna_nome] + '_prata'
      df.loc[i,coluna_valor] = tenta_dividir(texto_a_dividir=df.loc[i,coluna_valor],divisor='ouros',coluna=1)
      if coluna_energia_saude:
        df.loc[i,'Energia'] = tenta_dividir(texto_a_dividir=df.loc[i,coluna_energia_saude],coluna=2)
        df.loc[i,'Saude'] = tenta_dividir(texto_a_dividir=df.loc[i,coluna_energia_saude],coluna=3)
    if i % 4 == 2:
      df.loc[i,coluna_nome] = df.loc[i,coluna_nome] + '_ouro'
      df.loc[i,coluna_valor] = tenta_dividir(texto_a_dividir=df.loc[i,coluna_valor],divisor='ouros',coluna=2)
      if coluna_energia_saude:
        df.loc[i,'Energia'] = tenta_dividir(texto_a_dividir=df.loc[i,coluna_energia_saude],coluna=4)
        df.loc[i,'Saude'] = tenta_dividir(texto_a_dividir=df.loc[i,coluna_energia_saude],coluna=5)
    if i % 4 == 3:
      df.loc[i,coluna_nome] = df.loc[i,coluna_nome] + '_iridio'
      df.loc[i,coluna_valor] = tenta_dividir(texto_a_dividir=df.loc[i,coluna_valor],divisor='ouros',coluna=3)
      if coluna_energia_saude:
        df.loc[i,'Energia'] = tenta_dividir(texto_a_dividir=df.loc[i,coluna_energia_saude],coluna=6)
        df.loc[i,'Saude'] = tenta_dividir(texto_a_dividir=df.loc[i,coluna_energia_saude],coluna=7)
  return df

def extrair_valor_recompensa(df):
    """
    Extrai o valor da recompensa de um DataFrame.

    Args:
        df (pd.DataFrame): DataFrame de entrada.

    Returns:
        str ou None: Valor da recompensa, caso encontrado, caso contrário, None.
    """

    # Encontrar as colunas que contêm "Recompensa:"
    colunas_recompensa = df.columns[df.isin(['Recompensa:']).any()]

    # Se nenhuma coluna for encontrada, retornar None
    if len(colunas_recompensa) == 0:
        return None

    # Obter a coluna mais à direita
    coluna_recompensa = colunas_recompensa[-1]

    # Obter o índice da linha onde "Recompensa:" aparece na última coluna encontrada
    indice_recompensa = df[coluna_recompensa].eq('Recompensa:').idxmax()

    # Retornar o valor à direita da recompensa
    return df.iloc[indice_recompensa, df.columns.get_loc(coluna_recompensa) + 1]


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
  df_animais['Rendimento de venda'] = df_animais['Venda_5_coracoes'] / df_animais['Custo']
  df_animais['Rendimento de produção'] = df_animais['Custo'] / df_animais['Produz_valor']
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
      df_temp['Descrição'] = df_temp['Multiplicador de Munição'].apply(lambda x: 'Base de dano: ' + str(x))
      df_temp['Item'] = df_temp['Item'].apply(lambda linha: str(linha.replace('Todas as  ','').replace('  • Todos os ',', ').replace('"','')))
      df_temp.pop('Multiplicador de Munição')
    if arma == 'impossiveis':
      df_temp = df_temp.rename(columns={'Preço de venda':'Preço de Venda'})
    df_temp = df_temp.rename(columns={'Faixa de Dano Padrão': 'Dano', 
                                        'Item': 'Nome',
                                        'Chance de  Acerto Crítico': 'Chance de Acerto Crítico'})
    dfs_to_concat.append(df_temp)
  df_armas = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  df_armas['Preço de Compra'] = limpar_preco(df_armas['Preço de Compra'])
  df_armas['Preço de Venda'] = limpar_preco(df_armas['Preço de Venda'])
  df_armas = df_armas.drop(columns=['Unnamed: 0','Imagem'])
  df_armas = df_armas[['Nome','Tipo','Nível','Descrição','Dano','Chance de Acerto Crítico','Estatísticas','Localização','Preço de Compra','Preço de Venda']]
  df_armas['Dano médio'] = df_armas.Dano.apply(dano_medio)
  df_armas['Valor por dano'] = df_armas['Preço de Compra'] / df_armas['Dano médio']
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
  artefatos = artefatos.iloc[:,2:]
  artefatos['Preço'] = limpar_preco(artefatos['Preço'])
  artefatos.to_csv('docs_silver/artefatos.csv',encoding='utf-8')

  
  #artesanato
  lista_artesanatos = ['aneis',
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
  for artesanato in lista_artesanatos:
    df_temp = pd.read_csv(f'docs_bronze/artesanato_{artesanato}.csv')
    df_temp['Tipo'] = artesanato
    dfs_to_concat.append(df_temp)
  df_artesanatos = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  df_artesanatos = df_artesanatos.drop(columns=['Unnamed: 0','Imagem'])
  df_artesanatos = separar_quantidades_e_explodir(df_artesanatos,'Ingredientes')
  df_artesanatos = df_artesanatos[['Nome','Descrição','Tipo','Ingredientes_item','Ingredientes_qtd','Fonte da Receita','Origem da Receita','Dura Por','Energia','Saúde']]
  df_artesanatos.to_csv('docs_silver/artesanato.csv', encoding='utf-8')

  
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
  df_arvores.preco_muda_pierre = limpar_preco(df_arvores.preco_muda_pierre)
  df_arvores.preco_muda_carrinho_viagem = limpar_preco(df_arvores.preco_muda_carrinho_viagem)
  df_arvores['preco_minimo_muda_carrinho_viagem'] = df_arvores.preco_muda_carrinho_viagem.apply(precos_carrinho_viagem, minimo=True)
  df_arvores['preco_maximo_muda_carrinho_viagem'] = df_arvores.preco_muda_carrinho_viagem.apply(precos_carrinho_viagem, maximo=True)
  df_arvores['Preco_venda'] = df_arvores['Preco_venda'].astype(float)
  for linha in df_arvores.index:
    try:
      df_arvores.loc[linha,'Rentabilidade'] = round(df_arvores.loc[linha,'Preco_venda'] / df_arvores.loc[linha,'preco_muda_pierre'] * 1000,2)
    except ZeroDivisionError:
      df_arvores.loc[linha,'Rentabilidade'] = 0
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
                           'preco_muda_carrinho_viagem',
                           'preco_minimo_muda_carrinho_viagem',
                           'preco_maximo_muda_carrinho_viagem',
                           'Rentabilidade']]
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
  df_calendario['Dia'] = df_calendario['Dia'].apply(separar_dias)
  df_calendario = df_calendario.explode('Dia').reset_index(drop=True)
  df_calendario['Mes'] = df_calendario['Mes'].apply(lambda linha: linha.
                                                    replace('0.0.','0.').
                                                    replace('1.0.','1.').
                                                    replace('2.0.','2.'))
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
  lista_conjunto = ['2500','5000','10000','25000',
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
                 'primavera','verao','outono','inverno',
                 'peixes_especializados','peixes_lago','peixes_oceano','peixes_rio',
                 'pesca_covo','pesca_noturna',
                 'pesquisa_campo',
                 'plantacoes_primavera','plantacoes_verao','plantacoes_outono','plantacoes_qualidade',
                 'recursos_exoticos',
                 'tinta']
  dfs_to_concat = []
  for conjunto in lista_conjunto:
    df_temp = pd.read_csv(f'docs_bronze/conjunto_{conjunto}.csv')
    if conjunto == 'a_desaparecida':
      #corrigir posições das linhas 7 e 9 antes de alterar a coluna
      df_temp.iloc[7,2:3] = df_temp.iloc[7,0:1]
      df_temp.iloc[9,2:3] = df_temp.iloc[9,0:1]
      df_temp = df_temp.drop(index=[0,2,6,8]) #retira linhas
      df_temp['Recompensa'] = None #cria coluna Recompensa
    if conjunto in ['animal','a_desaparecida']: #retira 2 1ªs colunas
      df_temp = df_temp.iloc[:,2:]
    if len(df_temp.columns) >= 6:
      df_temp = df_temp.iloc[:,1:]
    # localiza valor de recompensa no dataframe
    df_temp['Recompensa'] = extrair_valor_recompensa(df_temp)
    #Repetir nome de coluna na primeira coluna
    df_temp.iloc[:,0] = df_temp.columns[1]
    #retirar a segunda coluna enquanto houver 5 ou mais colunas
    while len(df_temp.columns) >= 5:
      column_to_delete = df_temp.columns[1]
      df_temp = df_temp.drop(columns=column_to_delete)
    df_temp.columns = ['Conjunto','Requisitos','Descrição_requisitos','Recompensa']
    dfs_to_concat.append(df_temp)
  df_conjuntos = pd.concat(dfs_to_concat,ignore_index=True)
  df_conjuntos['Requisitos'] = df_conjuntos.apply(lambda row: row['Requisitos'] if not pd.isna(row['Requisitos']) else row['Descrição_requisitos'], axis=1)
  #retira linhas onde a coluna Requisitos tenha o valores inválidos
  df_conjuntos = df_conjuntos[~df_conjuntos.Requisitos.isin(['Recompensa:',''])]
  df_conjuntos = df_conjuntos.reset_index(drop=True)
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
  dfs_to_concat = [] 
  for culinaria in lista_culinaria:
    df_temp = pd.read_csv(f'docs_bronze/culinaria_{culinaria}.csv')
    #print(f'colunas de {culinaria}: {df_temp.columns}')
    df_temp = df_temp.rename(columns={'Necessário para:': 'Necessário para', 
                                      'Tempo de crescimento:': 'crescimento_produção',
                                      'Tempo de produção': 'crescimento_produção',
                                      'Tempo de Produção': 'crescimento_produção',
                                      'Quantidade Necessária':'Quantidade necessária',
                                      'Notas':'Descrição',
                                      'Localização':'Fonte',
                                      'Preço Unitário/Total': 'Preço de Venda',
                                      'Fonte da Receita':'Fonte'
                                      })
    dfs_to_concat.append(df_temp)
  df_culinaria = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  df_culinaria = df_culinaria.iloc[:,2:]
  df_culinaria['Energia'] = df_culinaria['Energia / Saúde'].apply(lambda row: tenta_dividir(texto_a_dividir=row,
                                                                                            divisor='  ',
                                                                                            coluna=0))
  df_culinaria['Saúde'] = df_culinaria['Energia / Saúde'].apply(lambda row: tenta_dividir(texto_a_dividir=row,
                                                                                            divisor='  ',
                                                                                            coluna=1))
  linhas_a_retirar = (df_culinaria['Fonte'].isna()) & (df_culinaria['Necessário para'].isna())
  df_culinaria = df_culinaria[~linhas_a_retirar]
  df_culinaria = df_culinaria.drop(columns='Energia / Saúde')
  df_culinaria.to_csv('docs_silver/culinaria.csv', encoding='utf-8')

  #custo_solo_concha
  solo_concha = pd.read_csv(f'docs_bronze\custo_solo_foliar_concha.csv', header=2,index_col='1')
  solo_concha = solo_concha.iloc[0:8,:]
  solo_concha['Tipo'] = 'Concha'
  solo_concha = solo_concha.rename(columns={'Qualidade da Concha':'Qualidade'})
  #custo_solo_coral
  solo_coral = pd.read_csv(f'docs_bronze\custo_solo_foliar_concha.csv', header=11,index_col='10')
  solo_coral['Tipo'] = 'Coral'
  solo_coral = solo_coral.rename(columns={'Qualidade do Coral':'Qualidade'})
  #concatena
  df_solo = pd.concat([solo_concha,solo_coral],ignore_index=True).reset_index(drop=True)
  df_solo.columns = ['Profissão','Qualidade','Artesanato','Pierre','Apagar','Tipo','Oásis']
  df_solo = df_solo[['Tipo','Qualidade','Profissão','Artesanato','Pierre','Oásis']]  
  df_solo.to_csv('docs_silver/solo_foliar.csv', encoding='utf-8')  

  #casa/estufa
  lista_casa = ['estagios',
                'estufa',
                'construcoes_melhoria',
                'construcoes_renovacoes',
                'construcoes_fazenda']
  dfs_to_concat = [] 
  for casa in lista_casa:
    df_temp = pd.read_csv(f'docs_bronze/casa_{casa}.csv', index_col='Unnamed: 0')
    if casa == 'estufa':
      df_temp = pd.read_csv(f'docs_bronze/casa_{casa}.csv', header=1)
      df_temp = df_temp.iloc[:,2].to_frame().T #seleciona a linha 2
      df_temp['Nome'] = 'Estufa'
    df_temp = df_temp.rename({'Estágio':'Nome','Mudanças':'Descrição',
                              1:'Descrição',2:'Detalhes',3:'Custo',5:'Tamanho',
                              'Name':'Nome','Description':'Descrição','Cost':'Custo'},axis=1)
    df_temp['Tipo'] = casa
    dfs_to_concat.append(df_temp)
  df_casa = pd.concat(dfs_to_concat, ignore_index=True).reset_index(drop=True)
  df_casa = df_casa[['Tipo','Nome','Custo','Animais','Descrição','Tamanho','Detalhes']]
  #df_casa = separar_quantidades_e_explodir(df= df_casa, coluna='Custo', divisor=')')
  df_casa.to_csv('docs_silver/casa.csv', encoding='utf-8')

  #ferramenta
  lista_ferramentas = ['efeitos','enxada','foice','lixeira','machado',
                      'picareta','regador','vara_pesca']
  dfs_to_concat = [] 
  for ferramenta in lista_ferramentas:
    df_temp = pd.read_csv(f'docs_bronze/ferramenta_{ferramenta}.csv')
    df_temp = df_temp.rename(columns={'Custo':'Preço',
                                      'Ingredientes':'Materiais',
                                      'Melhoras':'Efeito',
                                      'Melhorias':'Efeito',
                                      'Descrição':'Efeito'})
    df_temp['Tipo'] = ferramenta
    dfs_to_concat.append(df_temp)
  df_ferramentas = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  df_ferramentas = df_ferramentas[['Tipo','Nome','Efeito','Preço',
                                   'Materiais','Localização','Requisitos']]
  df_ferramentas.to_csv('docs_silver/ferramentas.csv', encoding='utf-8')
  

  #iscas
  df_iscas = pd.read_csv('docs_bronze\iscas.csv', encoding='utf-8')
  df_iscas = df_iscas.drop(columns=['Unnamed: 0','Imagem'])
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
                    'semente_couve_chinesa',
                    'semente_couve_flor',
                    'semente_couve',
                    'semente_fada',
                    'semente_girassol',
                    'semente_inhame',
                    'semente_jasmim_azul',
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
  dfs_to_concat = [] 
  for lavoura in lista_lavouras:
    df_temp = pd.read_csv(f'docs_bronze/lavoura_{lavoura}.csv')
    df_temp = df_temp.dropna(subset=['Semente'],ignore_index=True)
    dfs_to_concat.append(df_temp)    
  df_lavouras = pd.concat(dfs_to_concat*4,ignore_index=True).sort_values(by='Semente').reset_index(drop=True)
  df_lavouras.columns = ['Apagar',
                         'Crescimento estágio 1 (dias)','Crescimento estágio 2 (dias)','Crescimento estágio 3 (dias)',
                         'Tempo colheita (dias)','Tempo colheita continuado',
                         'Vende_por','Restaura',
                         'Usado em','Estação','Semente','Origem',
                         'Renda média (ouro por dia)',
                         'Crescimento estágio 4 (dias)','Crescimento estágio 5 (dias)']
  df_lavouras = divide_valores_por_qualidade(df = df_lavouras,coluna_nome='Semente',
                                             coluna_valor='Vende_por',coluna_energia_saude='Restaura')
  df_lavouras = df_lavouras[['Semente','Estação','Vende_por','Saude','Energia',
                             'Crescimento estágio 1 (dias)','Crescimento estágio 2 (dias)',
                             'Crescimento estágio 3 (dias)','Crescimento estágio 4 (dias)',
                             'Crescimento estágio 5 (dias)',
                             'Tempo colheita (dias)','Tempo colheita continuado',
                             'Renda média (ouro por dia)',
                             'Origem','Usado em']]
  df_lavouras.to_csv('docs_silver/lavouras.csv', encoding='utf-8')

  #lista_presente
  df_presentes = pd.read_csv('docs_bronze\lista_presentes.csv', encoding='utf-8', 
                             index_col='Unnamed: 0')
  df_presentes.to_csv('docs_silver/lista_presentes.csv', encoding='utf-8')

  #máquinas
  lista_maquinas = ['apiario',
                    'barril_madeira',
                    'barril',
                    'gerador_oleo',
                    'jarra_conserva',
                    'maquina_molho',
                    'prensa_queijo',
                    'maquina_maionese',
                    'tear']
  dfs_to_concat = []
  for maquina in lista_maquinas:
    df_temp = pd.read_csv(f'docs_bronze/mercadoria_{maquina}.csv')
    dfs_to_concat.append(df_temp)
  df_maquina = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  df_maquina = df_maquina[['Nome','Descrição','Ingredientes','Fonte da Receita']]
  df_maquina = df_maquina.dropna(subset=['Nome'],ignore_index=True)
  df_maquina = separar_quantidades_e_explodir(df_maquina,'Ingredientes')
  df_maquina.to_csv('docs_silver/maquinas.csv', encoding='utf-8')


  #mercadorias
  lista_mercadorias = ['mel',
                      'produto_barril_madeira',
                      'produto_barril',
                      'produto_gerador_oleo',
                      'produto_jarra_conserva',
                      'produto_maquina_molho',
                      'produto_prensa_queijo',
                      'produto_maquina_maionese',
                      'produto_tear']
  dfs_to_concat = [] 
  for mercadoria in lista_mercadorias:
    df_temp = pd.read_csv(f'docs_bronze/mercadoria_{mercadoria}.csv')
    df_temp = df_temp.rename(columns={'Energia':'Energia/Saúde',
                                      'Energia/Saúde/Bônus':'Energia/Saúde',
                                      'Restaura':'Energia/Saúde',
                                      'Preço de Venda Base': 'Venda (ouros)',
                                      'Valor de venda':'Venda (ouros)',
                                      'Preço da Venda':'Venda (ouros)',
                                      'Preço de venda':'Venda (ouros)',
                                      'Image':'Imagem',
                                      'Name':'Nome',
                                      'Ingrediente':'Ingredientes'})
    dfs_to_concat.append(df_temp)
  df_mercadorias = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  df_mercadorias = df_mercadorias.drop(columns=['Unnamed: 0','Imagem','0','1'])
  df_mercadorias = df_mercadorias.sort_values(by='Nome').reset_index(drop=True)
  #preencher valores nulos de outras colunas onde houver mesmos valores na coluna 'Nome'
  for nome in df_mercadorias['Nome'].unique():
    if nome == 'Óleo':
      pass
    else:
      df_mercadorias.loc[df_mercadorias['Nome'] == nome] = df_mercadorias.loc[df_mercadorias['Nome'] == nome].fillna(method='bfill')
      df_mercadorias.loc[df_mercadorias['Nome'] == nome] = df_mercadorias.loc[df_mercadorias['Nome'] == nome].drop_duplicates(subset='Nome',keep='first')
  df_mercadorias = df_mercadorias.dropna(subset=['Descrição'],ignore_index=True).reset_index(drop=True)
  df_mercadorias.to_csv('docs_silver/mercadorias.csv', encoding='utf-8')

  #minerais
  lista_minerais = ['coleta',
                    'gemas',
                    'geodos',
                    'origem_geodos']
  dfs_to_concat = [] 
  for mineral in lista_minerais:
    df_temp = pd.read_csv(f'docs_bronze/minerais_{mineral}.csv')
    df_temp = df_temp.rename(columns={'Usado Em':'Usado em'})
    dfs_to_concat.append(df_temp)  
  dfs_to_concat.append(pd.read_csv('docs_bronze/nos_minerio.csv').rename(columns={'Local':'Localização'}))
  df_minerais = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  df_minerais['Preço de Venda'] = limpar_preco(serie=df_minerais['Preço de Venda'])
  df_minerais = df_minerais.drop(columns=['Unnamed: 0','Imagem','imagem'])
  df_minerais.to_csv('docs_silver/minerais.csv', encoding='utf-8')

  #missao
  lista_missoes = ['_especiais_sr_qi',
                    '_itens_lista',
                    '_lista',
                    '_pedidos_especiais',
                    '']
  dfs_to_concat = [] 
  for missao in lista_missoes:
    df_temp = pd.read_csv(f'docs_bronze/missoes{missao}.csv')
    df_temp = df_temp.rename(columns={'Texto da Missão':'Descrição',
                                      'Missão Relacionada':'Requisitos',
                                      'Requerimentos':'Requisitos',
                                      '0':'Nome da Missão',
                                      '1':'Descrição',
                                      'Missão Relacionada':'Nome da Missão'})
    df_temp['Tipo'] = missao[1:].replace('_',' ').capitalize()
    dfs_to_concat.append(df_temp)
  df_missoes = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  df_missoes = df_missoes.drop(columns=['Unnamed: 0','Imagem'])
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
                    'itens_especiais1',
                    'itens_especiais2',
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
                    'plantas_decorativas_sazonais',
                    'poltronas',
                    'posteres',
                    'sofas',
                    'tapetes',
                    'tochas',
                    'tvs']
  dfs_to_concat = [] 
  for mobilia in lista_mobilias:
    if mobilia == 'tapetes':
      df_temp = pd.read_csv(f'docs_bronze/mobilia_{mobilia}.csv', header=2)
      df_temp.columns = ['index','Nome','carpintaria(ouros)','carrinho_viagem(ouros)','pierre(ouros)','oasis','Tamanho']
      df_temp = df_temp.melt(id_vars=['Nome','Tamanho'], 
                             value_vars=['carpintaria(ouros)', 'carrinho_viagem(ouros)', 'pierre(ouros)', 'oasis'],
                             var_name='Loja', value_name='Preço')
    else:
      df_temp = pd.read_csv(f'docs_bronze/mobilia_{mobilia}.csv')
    if mobilia == 'aquarios':
          df_temp.columns = ['index','Nome', 'peixaria(ouros)', 'catalogo(ouros)', 'qi(diamantes)']
          df_temp = df_temp.melt(id_vars=['Nome'], value_vars=['peixaria(ouros)', 'catalogo(ouros)', 'qi(diamantes)'], 
                                var_name='Loja', value_name='Preço')
    if mobilia in ['sofas','cadeiras1','cadeiras2','cadeiras3',
                      'bancos','mesas1','mesas2','mesas3','estantes',
                      'diversos1','diversos2']:
      df_temp['Loja'] = 'carpintaria(ouros)'
    if mobilia == 'mesas_longas':
      df_temp.columns = ['index','Nome', 'carpintaria(ouros)', 'festivais(ouros)']
      df_temp = df_temp.melt(id_vars=['Nome'], value_vars=['carpintaria(ouros)', 'festivais(ouros)'],
                            var_name='Loja', value_name='Preço')
    if mobilia == 'lareiras':
      df_temp.columns = ['index','Nome', 'carpintaria(ouros)', 'outros']
      df_temp = df_temp.melt(id_vars=['Nome'], value_vars=['carpintaria(ouros)', 'outros'],
                            var_name='Loja', value_name='Preço')
    if mobilia == 'lampadas':
      df_temp.columns = ['index','Nome', 'carpintaria(ouros)', 'carrinho_viagem(ouros)','oasis']
      df_temp = df_temp.melt(id_vars=['Nome'], value_vars=['carpintaria(ouros)','carrinho_viagem(ouros)','oasis'],
                            var_name='Loja', value_name='Preço')
    if mobilia == 'janelas':
      df_temp.columns = ['index','Nome', 'carpintaria(ouros)', 'pierre(ouros)']
      df_temp = df_temp.melt(id_vars=['Nome'], value_vars=['carpintaria(ouros)', 'pierre(ouros)'],
                            var_name='Loja', value_name='Preço')
    if mobilia == 'tvs':
      df_temp.columns = ['index','Nome', 'carpintaria(ouros)', 'comerciante_ilhas(inhame_coco)']
      df_temp = df_temp.melt(id_vars=['Nome'], value_vars=['carpintaria(ouros)', 'comerciante_ilhas(inhame_coco)'],
                            var_name='Loja', value_name='Preço')
    if mobilia in ['plantas_decorativas_chao1','plantas_decorativas_chao2']:
      df_temp.columns = ['index','Nome', 'carpintaria(ouros)', 'carrinho_viagem(ouros)']
      df_temp = df_temp.melt(id_vars=['Nome'], value_vars=['carpintaria(ouros)', 'carrinho_viagem(ouros)'],
                            var_name='Loja', value_name='Preço')
    if mobilia == 'plantas_decorativas_sazonais':
      df_temp = df_temp[['Também vendido por','Preço']].rename(columns={'Também vendido por':'Loja'})
      df_temp['Nome'] = 'sazonal' + df_temp.index.astype(str)
    if mobilia == 'pinturas':
      df_temp = pd.read_csv(f'docs_bronze/mobilia_{mobilia}.csv', header=2)
      df_temp.columns = ['index','Nome','carpintaria(ouros)','cassino(qicoin)','carrinho_viagem(ouros)','pierre(ouros)','oasis(ouros)']
      df_temp = df_temp.melt(id_vars=['Nome'], value_vars=['carpintaria(ouros)','cassino(qicoin)','carrinho_viagem(ouros)','pierre(ouros)','oasis(ouros)'],
                            var_name='Loja', value_name='Preço')
    if mobilia == 'decoracao_parede':
      df_temp.columns = ['index','Nome', 'carpintaria(ouros)', 'carrinho_viagem(ouros)','catalogo(ouros)']
      df_temp = df_temp.melt(id_vars=['Nome'], value_vars=['carpintaria(ouros)','carrinho_viagem(ouros)','catalogo(ouros)'],
                            var_name='Loja', value_name='Preço')
    if mobilia == 'decoracao_parede2':
      df_temp.columns = ['Nome',
                         'pierre_festival_ovo(ouros)',
                         'pierre_festival_medusas_lua(ouros)',
                         'pierre_festival_estrela_invernal(ouros)',
                         'catalogo(ouros)']
      df_temp = df_temp.melt(id_vars=['Nome'], value_vars=['pierre_festival_ovo(ouros)',
                         'pierre_festival_medusas_lua(ouros)',
                         'pierre_festival_estrela_invernal(ouros)',
                         'catalogo(ouros)'],
                            var_name='Loja', value_name='Preço')
    df_temp['Tipo'] = mobilia
    df_temp = df_temp.rename(columns={'Item':'Nome',
                                      'Origem':'Loja',
                                      'Como obter':'Loja',
                                      'Onde obter':'Loja',
                                      'Preço de Compra':'Preço'})
    dfs_to_concat.append(df_temp)
  df_mobilias = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  # Aplicar a função para extrair valor e moeda
  df_mobilias[['valor', 'moeda']] = df_mobilias['Preço'].apply(lambda x: pd.Series(extrair_valor_moeda(x)))
  #falta separar preço na coluna preço e loja pelo termo 'por'
  #nome composto 'Fragmento de Fogo' não separou corretamente
  #retirar espaço no meio dos números de valores acima de 1000
  #editar colunas de loja para não precisar colocar nome da moeda  
  df_mobilias = df_mobilias.drop(columns=['Unnamed: 0','Imagem'])
  df_mobilias['Tipo'] = df_mobilias['Tipo'].apply(lambda row: row.replace('1','').replace('2','').replace('3',''))
  df_mobilias['Nome'] = df_mobilias['Nome'].apply(lambda row: row.replace("'","").replace('"',''))
  df_mobilias.to_csv('docs_silver/mobilias.csv', encoding='utf-8')

  #peixes
  lista_peixes = ['covo',
                  'itens_pescaveis',
                  'lendarios',
                  'lendarios_ii',
                  'mercado_noturno']
  dfs_to_concat = [] 
  for peixe in lista_peixes:
    if peixe == 'covo':
      df_temp = pd.read_csv(f'docs_bronze/peixes_{peixe}.csv', header=1)
    else:
      df_temp = pd.read_csv(f'docs_bronze/peixes_{peixe}.csv')
    df_temp = df_temp.dropna(subset=['Descrição'],ignore_index=True)
    df_temp['Tipo'] = peixe
    dfs_to_concat.append(df_temp)
  df_peixes = pd.concat(dfs_to_concat*4,ignore_index=True).reset_index(drop=True)
  df_peixes = df_peixes.drop(columns=['Unnamed: 0','Imagem','Image'])
  df_peixes = df_peixes.rename(columns={'Preço de Venda':'Venda'})
  df_peixes = df_peixes.sort_values(by='Nome').reset_index(drop=True)
  df_peixes = divide_valores_por_qualidade(df = df_peixes, #falta explodir Marinheiro e Não-marinheiro junto ver multiplicação
                                           coluna_nome='Nome',
                                           coluna_valor=['Preço','Marinheiro','Não-marinheiro'])
  df_peixes.to_csv('docs_silver/peixes.csv', encoding='utf-8')

  #pesca #baús
  pescas_bau = pd.read_csv(f'docs_bronze/pesca_bau.csv')
  #df_temp = df_temp.rename(columns={'Preço de Venda':'Preço'})
  pescas_bau.to_csv('docs_silver/pescas_bau.csv', encoding='utf-8')
  pescas_zona = pd.read_csv(f'docs_bronze/pesca_zona.csv')
  pescas_zona.columns = ['Apagar', 'Zona de Pesca', 'Nível de Pesca', 
                         'Tamanho mínimo de peixe','Tamanho máximo de peixe',
                         '% Qualidade Normal','% Qualidade Prata', '% Qualidade Ouro',
                         'Tamanho do Sardinha Perfeita (cm)',
                         'Tamanho do Arenque Perfeito (cm)']
  pescas_zona = pescas_zona.drop(index=0)
  pescas_zona = pescas_zona.drop(columns=['Apagar'])
  pescas_zona.to_csv('docs_silver/pescas_zona.csv', encoding='utf-8')

  #solos_producao
  df_solos_producao = pd.read_csv('docs_bronze\solos_producao.csv', encoding='utf-8')
  df_solos_producao = df_solos_producao.drop(columns=['Unnamed: 0'])
  df_solos_producao.to_csv('docs_silver\solos_producao.csv', encoding='utf-8')
  
  #taxa_cultivo
  lista_taxas_cultivo = ['solo_normal',
                        'fertilizante_basico',
                        'fertilizante_qualidade',
                        'fertilizante_premium']
  dfs_to_concat = [] 
  i = 1
  for taxa in lista_taxas_cultivo:
    df_temp = pd.read_csv(f'docs_bronze/taxa_cultivo_{taxa}.csv')
    df_temp['Tipo'] = str(i) + '.' + taxa
    dfs_to_concat.append(df_temp)
    i += 1
  df_taxas_cultivo = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  df_taxas_cultivo = df_taxas_cultivo.drop(columns=['Unnamed: 0'])
  #ordenar por nível de cultivo e secundariamente por tipo
  df_taxas_cultivo = df_taxas_cultivo.sort_values(by=['Tipo']).sort_values(by=['Nível de Cultivo']).reset_index(drop=True)
  df_taxas_cultivo = df_taxas_cultivo[['Nível de Cultivo', 'Tipo', 'Preço médio',
                                       '% Qualidade Normal', '% Qualidade Prata',
                                       '% Qualidade Ouro', '% Qualidade Irídio']]
  df_taxas_cultivo.to_csv('docs_silver/taxas_cultivo.csv', encoding='utf-8')

  # Lojas e estoques

  #comidas

  pass




if __name__ == '__main__':
  import pandas as pd
  import re
  

  profissoes()
  limpar_csv('docs_bronze/xp_coleta.csv')
  xp()
  concat_dataframes()
