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
  coleta.item[0:3] = coleta.item[0:3].apply(lambda linha: linha.split('por')[1])
  coleta.item[5] = coleta.item[5].split('para')[1]
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

  df_animais = df_animais[['Nome','Custo','Requisitos','Produz','Venda_5_coracoes']]  
  df_animais.to_csv('docs_silver/animais.csv', encoding='utf-8')

  #armas
  lista_armas = ['adagas',
                'clavas',
                'espadas',
                'estilingues',
                'impossiveis',
                'luta_atributos',
                'municoes']
  #padronizar colunas
  dfs_to_concat = [] 
  for arma in lista_armas:
    df_temp = pd.read_csv(f'docs_bronze/armas_{arma}.csv')
    print(f'colunas de {arma}: {df_temp.columns}')
    dfs_to_concat.append(df_temp)
  df_armas = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  df_armas.to_csv('docs_silver/armas.csv', encoding='utf-8')

  #artefatos
  artefato_tesouro = pd.read_csv('docs_bronze/artefatos_tesouro.csv')
  artefatos = pd.read_csv('docs_bronze/artefatos.csv')
  artefato_tesouro.columns = ['','Imagem','Nome','Descrição','Local']
  lista_artefatos = [artefatos,artefato_tesouro]
  artefatos = pd.concat(lista_artefatos,ignore_index=True)
  artefatos = artefato_tesouro[['Nome','Descrição','Preço','Local']]
  print(artefatos)

  #artesanato
  lista_artesanato = ['aneis',
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
  #padronizar colunas
  dfs_to_concat = [] 
  for artesanato in lista_artesanato:
    df_temp = pd.read_csv(f'docs_bronze/artesanato_{artesanato}.csv')
    print(f'colunas de {artesanato}: {df_temp.columns}')
    dfs_to_concat.append(df_temp)
  df_artesanatos = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  df_artesanatos.to_csv('docs_silver/artesanatos.csv', encoding='utf-8')

    #arvores
  lista_arvores: list = ['bananeira',
                         'cerejeira',
                         'damasqueiro',
                         'laranjeira',
                         'macieira',
                         'mangurira',
                         'pessegueira',
                         'romanzeira']
  #padronizar colunas
  dfs_to_concat = [] 
  for arvore in lista_arvores:
    df_temp = pd.read_csv(f'docs_bronze/arvores_{artesanato}.csv')
    df_temp = df_temp.loc[1,:].reindex()
    df_temp_muda = pd.read_csv(f'docs_bronze/arvores_muda_{artesanato}.csv')
    df_temp_muda = df_temp_muda.loc[0,:].reindex()
    #concatenar árvore e muda em novas colunas
    df_temp.join(df_temp_muda)
    print(f'colunas de {arvore}: {df_temp.columns}')
    dfs_to_concat.append(df_temp)
  df_arvores = pd.concat(dfs_to_concat,ignore_index=True).reset_index(drop=True)
  df_arvores.to_csv('docs_silver/arvores.csv', encoding='utf-8')
  #calendario

  #vestuario

  #carteira

  #coleta

  #conjunto

  #culinaria

  #custo_solo

  #casa/estufa

  #ferramenta

  #lavoura

  #lista_presente

  #mercadoria

  #minerais

  #missao

  #mobilia

  #nos_minerio

  #peixes

  #pesca

  #taxa_cultivo

  
  pass




if __name__ == '__main__':
  import pandas as pd
  #profissoes()
  #limpar_csv('docs_bronze/xp_coleta.csv')
  #xp()
  concat_dataframes()



"""def grafico_xp ():
  #xp cultivo
  sns.boxplot(data=df_xp_cultivos, y='Estacao', x='XP', hue='Estacao')

  df_xp_cultivos = df_xp_cultivos.sort_values(by='XP', ascending=False)
  with sns.axes_style('whitegrid'):
    grafico = sns.barplot(data=df_xp_cultivos, y='Cultivo', x='XP', hue='Estacao', width = 0.8)
    grafico.set_title('XP por cultivo')
    grafico.set_xlabel('XP')
    grafico.set_ylabel('Cultivo')
    #tamanho do gráfico
    grafico.figure.set_size_inches(10, 20)
    
  #qualidade cultivo
  #fixar cores da legenda
  
  pass



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

