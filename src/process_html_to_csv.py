def df_cultivo(html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html_cultivo = f.read()
    
    sopa = bs4(html_cultivo, 'html.parser')


    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela))))#, parser='lxml'))

    profissao_cultivo = lista[0][0] #0 Cultivo

    #transformar linhas 3 a 6 em novas colunas na profissao_cultivo
    profissao_cultivo_cont = profissao_cultivo[3:].reset_index(drop=True)
    profissao_cultivo_cont.columns = profissao_cultivo_cont.iloc[0]
    profissao_cultivo_cont = profissao_cultivo_cont[1:].reset_index(drop=True)


    #adicionar colunas em profissao_cultivo
    profissao_cultivo = profissao_cultivo[:3]
    profissao_cultivo = pd.concat([profissao_cultivo, profissao_cultivo_cont], axis=1)
    profissao_cultivo['profissao'] = 'cultivo'

    del profissao_cultivo_cont


    profissao_cultivo.to_csv("docs_bronze/profissao_cultivo.csv")

    #df_solos
    solo_normal = lista[2][0]
    solo_fertilizante_basico = lista[3][0]
    solo_fertilizante_qualidade = lista[4][0]

    solo_normal['Melhoramento'] = 'Normal'
    solo_fertilizante_basico['Melhoramento'] = 'Fertilizante Básico'
    solo_fertilizante_qualidade['Melhoramento'] = 'Fertilizante de Qualidade'

    # concatenar dataframes
    df_solos = solo_normal.merge(solo_fertilizante_basico, how='outer').merge(solo_fertilizante_qualidade, how='outer')

    #apagar dataframes originais da memória
    del solo_normal
    del solo_fertilizante_basico
    del solo_fertilizante_qualidade

    df_solos = df_solos[['Melhoramento', 'Nível Cultivo', '% Qual. Regular', '% Qual. Prata', '% Qual. Ouro']]
    df_solos = df_solos.rename(columns={'Nível Cultivo': 'nivel_habilidade_cultivo',
                                        '% Qual. Regular': 'qualidade_regular',
                                        '% Qual. Prata':'qualidade_prata',
                                        '% Qual. Ouro': 'qualidade_ouro'})

    # separar colunas qualidade_regular, qualidade_prata e qualidade_ouro em cada tabela e adicionar à coluna
    df_solos_regular = df_solos[['Melhoramento','nivel_habilidade_cultivo','qualidade_regular']]
    df_solos_regular['qualidade_produto'] = '1.regular'
    df_solos_regular = df_solos_regular.rename(columns={'qualidade_regular': 'percentual'})

    df_solos_prata = df_solos[['Melhoramento','nivel_habilidade_cultivo','qualidade_prata']]
    df_solos_prata['qualidade_produto'] = '2.prata'
    df_solos_prata = df_solos_prata.rename(columns={'qualidade_prata': 'percentual'})

    df_solos_ouro = df_solos[['Melhoramento','nivel_habilidade_cultivo','qualidade_ouro']]
    df_solos_ouro['qualidade_produto'] = '3.ouro'
    df_solos_ouro = df_solos_ouro.rename(columns={'qualidade_ouro': 'percentual'})

    #concatenar
    df_solos = pd.concat([df_solos_regular, df_solos_prata, df_solos_ouro])

    del df_solos_regular
    del df_solos_prata
    del df_solos_ouro

    #ordenar e resetar index
    df_solos = df_solos.sort_values(by=['qualidade_produto']).sort_values(by=['nivel_habilidade_cultivo']).reset_index(drop=True)

    #corrigir tipos de dados nas colunas
    df_solos['percentual'] = df_solos['percentual'].replace('%', '', regex=True).astype(int)
    df_solos['nivel_habilidade_cultivo'] = df_solos['nivel_habilidade_cultivo'].astype(str)

    #reordenar colunas
    df_solos = df_solos[['nivel_habilidade_cultivo','Melhoramento','qualidade_produto','percentual']]
    df_solos.to_csv('docs_bronze/solos_producao.csv')
    
    #xp_cultivos
    xp_cultivo_primavera = lista[5][0]
    xp_cultivo_verao = lista[6][0]
    xp_cultivo_outono = lista[7][0]
    xp_chirivia = lista[8][0]

    #transformar coluna MultiIndex em normal
    xp_cultivo_primavera.columns = xp_cultivo_primavera.columns.droplevel()
    xp_cultivo_verao.columns = xp_cultivo_verao.columns.droplevel()
    xp_cultivo_outono.columns = xp_cultivo_outono.columns.droplevel()

    #adicionar coluna estação
    xp_cultivo_primavera['Estacao'] = 'Primavera'
    xp_cultivo_verao['Estacao'] = 'Verão'
    xp_cultivo_outono['Estacao'] = 'Outono'
    xp_chirivia['Estacao'] = 'Primavera'
    
    #adaptando chirivias aos outros dataframes
    xp_chirivia['XP'] = round(xp_chirivia['Experiência'] / xp_chirivia['Chirivias Colhidas no Total'],0)
    xp_chirivia['Cultivo'] = xp_chirivia['Chirivias Colhidas no Total'].apply(lambda linha: f'Cada 1 das {linha} Chirivias coletadas')
    print(xp_chirivia)
    xp_chirivia = xp_chirivia[['Estacao', 'XP', 'Cultivo']]

    #merge dfs
    df_xp_cultivos = xp_cultivo_primavera.merge(xp_cultivo_verao, how='outer')
    df_xp_cultivos = df_xp_cultivos.merge(xp_cultivo_outono, how='outer')
    print(df_xp_cultivos)
    df_xp_cultivos = df_xp_cultivos.merge(xp_chirivia, how='outer')
    print(df_xp_cultivos)

    #apagar dataframes concatenados
    del xp_cultivo_primavera
    del xp_cultivo_verao
    del xp_cultivo_outono
    del xp_chirivia

    df_xp_cultivos['Profissao'] = 'cultivo'

    #reordenar colunas
    df_xp_cultivos = df_xp_cultivos[['Profissao','Estacao','Cultivo','XP']]
    
    #salvar em csv
    df_xp_cultivos.to_csv('docs_bronze/xp_cultivo.csv')

    
    pass

def df_mineracao(html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html_mineracao = f.read()
    
    sopa = bs4(html_mineracao, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela))))#, parser='lxml')) #só funciona se ativar .venv

    profissao_mineracao = lista[0][0]

    #transformar linhas 3 a 6 em novas colunas na profissao_mineracao
    profissao_mineracao_cont = profissao_mineracao[3:].reset_index(drop=True)
    profissao_mineracao_cont.columns = profissao_mineracao_cont.iloc[0]
    profissao_mineracao_cont = profissao_mineracao_cont[1:].reset_index(drop=True)

    #adicionar colunas em profissao_cultivo
    profissao_mineracao = profissao_mineracao[:3]
    profissao_mineracao = pd.concat([profissao_mineracao, profissao_mineracao_cont], axis=1)

    profissao_mineracao['profissao'] = 'mineracao'

    #apagar dataframes originais da memória
    del profissao_mineracao_cont

    profissao_mineracao.to_csv('docs_bronze/profissao_mineracao.csv')

    xp_mineracao = lista[1][0]
    xp_mineracao.to_csv('docs_bronze/xp_mineracao.csv')

    nos_minerio = lista[3][0]
    nos_minerio.to_csv('docs_bronze/nos_minerio.csv')




if __name__ == '__main__':
    #import
    from bs4 import BeautifulSoup as bs4
    import pandas as pd
    from io import StringIO

    #execute
    #df_cultivo(html='docs_raw/sopa_Cultivo.html')
    df_mineracao(html='docs_raw/sopa_Mineração.html')
    