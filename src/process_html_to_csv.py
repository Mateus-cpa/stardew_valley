def df_cultivo(html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')


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
    xp_chirivia = xp_chirivia[['Estacao', 'XP', 'Cultivo']]

    #merge dfs
    df_xp_cultivos = xp_cultivo_primavera.merge(xp_cultivo_verao, how='outer')
    df_xp_cultivos = df_xp_cultivos.merge(xp_cultivo_outono, how='outer')
    df_xp_cultivos = df_xp_cultivos.merge(xp_chirivia, how='outer')
    
    df_xp_cultivos['Profissao'] = 'cultivo'

    #reordenar colunas
    df_xp_cultivos = df_xp_cultivos[['Profissao','Estacao','Cultivo','XP']]
    
    #salvar em csv
    df_xp_cultivos.to_csv('docs_bronze/xp_cultivo.csv')

    
    pass

def df_mineracao(html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

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

def df_coleta(html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

    profissao_coleta = lista[0][0]

        
    #transformar linhas 3 a 6 em novas colunas na profissao_coleta
    profissao_coleta_cont = profissao_coleta[3:].reset_index(drop=True)
    profissao_coleta_cont.columns = profissao_coleta_cont.iloc[0]
    profissao_coleta_cont = profissao_coleta_cont[1:].reset_index(drop=True)

    #adicionar colunas em profissao_cultivo
    profissao_coleta = profissao_coleta[:3]
    profissao_coleta = pd.concat([profissao_coleta, profissao_coleta_cont], axis=1)
    profissao_coleta['profissao'] = 'coleta'


    profissao_coleta.to_csv('docs_bronze/profissao_coleta.csv')

    seiva_coleta = lista[3][0]
    seiva_coleta['origem'] = 'seiva'
    seiva_coleta.Efeito = seiva_coleta.Efeito.str.replace('−', '-') #substituir todos − por -
    seiva_coleta.to_csv('docs_bronze/coleta_seiva.csv')

    primavera_coleta = lista[5][0]
    primavera_coleta = primavera_coleta[~primavera_coleta['Descrição'].isna()]
    primavera_coleta['origem'] = 'primavera'
    primavera_coleta.to_csv('docs_bronze/coleta_primavera.csv')

    verao_coleta = lista[22][0]
    verao_coleta = verao_coleta[~verao_coleta['Descrição'].isna()]
    verao_coleta = verao_coleta.rename(columns={'Recupera': 'Efeito'})
    verao_coleta['origem'] = 'verao'
    verao_coleta.to_csv('docs_bronze/coleta_verao.csv')

    outono_coleta = lista[33][0]
    outono_coleta = outono_coleta[~outono_coleta['Descrição'].isna()]
    outono_coleta = outono_coleta.rename(columns={'Recupera': 'Efeito'})
    outono_coleta['origem'] = 'outono'
    outono_coleta.to_csv('docs_bronze/coleta_outono.csv')

    inverno_coleta = lista[46][0]
    inverno_coleta = inverno_coleta[~inverno_coleta['Descrição'].isna()]
    inverno_coleta = inverno_coleta.rename(columns={'Recupera': 'Efeito'})
    inverno_coleta['origem'] = 'inverno'
    inverno_coleta.to_csv('docs_bronze/coleta_inverno.csv')

    praia_coleta = lista[57][0]
    praia_coleta = praia_coleta[~praia_coleta['Descrição'].isna()]
    praia_coleta['origem'] = 'praia'
    praia_coleta.to_csv('docs_bronze/coleta_praia.csv')

    cavernas_coleta = lista[67][0]
    cavernas_coleta = cavernas_coleta[~cavernas_coleta['Descrição'].isna()]
    cavernas_coleta = cavernas_coleta.rename(columns={'Recupera': 'Efeito'})
    cavernas_coleta['origem'] = 'cavernas'
    cavernas_coleta.to_csv('docs_bronze/coleta_cavernas.csv')

    deserto_coleta = lista[74][0]
    deserto_coleta = deserto_coleta[~deserto_coleta['Descrição'].isna()]
    deserto_coleta = deserto_coleta.rename(columns={'Recupera': 'Efeito'})
    deserto_coleta['origem'] = 'deserto'
    deserto_coleta.to_csv('docs_bronze/coleta_deserto.csv')

    ilha_gengibre_coleta = lista[78][0]
    ilha_gengibre_coleta = ilha_gengibre_coleta[~ilha_gengibre_coleta['Descrição'].isna()]
    ilha_gengibre_coleta = ilha_gengibre_coleta.rename(columns={'Recupera': 'Efeito'})
    ilha_gengibre_coleta['origem'] = 'ilha gengibre'
    ilha_gengibre_coleta.to_csv('docs_bronze/coleta_ilha_gengibre.csv')

    lista = []
    for item in sopa.find_all('li'):
        lista.append(item.text)
 
      
    #salvar linhas 27 a 39 de lista no dataframe, cada um em uma linha
    xp_coleta = pd.DataFrame(lista[27:40])
    xp_coleta.columns = ['item']
    xp_coleta['item'] = xp_coleta.item.apply(lambda x: x.replace('\n','')) #retira quebras de linha
    xp_coleta['item'] = xp_coleta.item.str.split().agg(" ".join) #retira espaços múltiplos entre as palavras
                                     
    xp_coleta.to_csv('docs_bronze/xp_coleta.csv')

    pass

def df_pesca(html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

    profissao_pesca = lista[3][0]


    #transformar linhas 3 a 6 em novas colunas na profissao_coleta
    profissao_pesca_cont = profissao_pesca[3:].reset_index(drop=True)
    profissao_pesca_cont.columns = profissao_pesca_cont.iloc[0]
    profissao_pesca_cont = profissao_pesca_cont[1:].reset_index(drop=True)


    #adicionar colunas em profissao_cultivo
    profissao_pesca = profissao_pesca[:3]
    profissao_pesca = pd.concat([profissao_pesca, profissao_pesca_cont], axis=1)

    profissao_pesca['profissao'] = 'pesca'

    profissao_pesca.to_csv('docs_bronze/profissao_pesca.csv')

    zona_pesca = lista[1][0]
    zona_pesca.to_csv('docs_bronze/pesca_zona.csv')
    varas_pesca = lista[2][0]
    varas_pesca.to_csv('docs_bronze/pesca_varas_pesca.csv')
    xp_pesca = lista[4][0]
    xp_pesca.to_csv('docs_bronze/xp_pesca.csv')
    comida_pesca = lista[5][0]
    comida_pesca = comida_pesca[~comida_pesca['Descrição'].isna()]
    comida_pesca.to_csv('docs_bronze/pesca_comida.csv')
    bau_pesca = lista[9][0]
    bau_pesca.to_csv('docs_bronze/pesca_bau.csv')

    pass

def df_combate(html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html_combate = f.read()
    
    sopa = bs4(html_combate, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

    profissao_combate = lista[0][0]

    #transformar linhas 3 a 6 em novas colunas na profissao_coleta
    profissao_combate_cont = profissao_combate[3:].reset_index(drop=True)
    profissao_combate_cont.columns = profissao_combate_cont.iloc[0]
    profissao_combate_cont = profissao_combate_cont[1:].reset_index(drop=True)


    #adicionar colunas em profissao_cultivo
    profissao_combate = profissao_combate[:3]
    profissao_combate = pd.concat([profissao_combate, profissao_combate_cont], axis=1)

    profissao_combate['profissao'] = 'combate'

    profissao_combate.to_csv('docs_bronze/profissao_combate.csv')

    xp_combate = lista[1][0]
    xp_combate.to_csv('docs_bronze/xp_combate.csv')
def extrair_valor_ouro(ultima_linha):
    for celula in ultima_linha:
        if 'ouro' in str(celula):
            celula = celula.split('ouro')[0].split(' ')[-1]
            celula = celula.replace('≈',',').replace(',','.').replace('-','')
            celula = celula.strip()
            return celula

def df_lavouras(html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv
    # primavera
    semente_alho = lista[1][0]
    semente_alho['Estação'] = 'Primavera'
    semente_alho.to_csv('docs_bronze/lavoura_semente_alho.csv')
    semente_arroz = lista[5][0]
    semente_arroz['Estação'] = 'Primavera'
    semente_arroz.to_csv('docs_bronze/lavoura_semente_arroz.csv')
    semente_batata = lista[8][0]
    semente_batata['Estação'] = 'Primavera'
    semente_batata.to_csv('docs_bronze/lavoura_semente_batata.csv')
    semente_cenoura = lista[12][0]
    semente_cenoura['Estação'] = 'Primavera'
    semente_cenoura.to_csv('docs_bronze/lavoura_semente_cenoura.csv')
    semente_chirivia = lista[16][0]
    semente_chirivia['Estação'] = 'Primavera'
    semente_chirivia.to_csv('docs_bronze/lavoura_semente_chirivia.csv')
    semente_couve = lista[20][0]
    semente_couve['Estação'] = 'Primavera'
    semente_couve.to_csv('docs_bronze/lavoura_semente_couve.csv')
    semente_couve_flor = lista[24][0]
    semente_couve_flor['Estação'] = 'Primavera'
    semente_couve_flor.to_csv('docs_bronze/lavoura_semente_couve_flor.csv')
    grao_cafe = lista[28][0]
    grao_cafe['Estação'] = 'Primavera'
    grao_cafe.to_csv('docs_bronze/lavoura_grao_cafe.csv')
    semente_jasmim_azul = lista[31][0]
    semente_jasmim_azul['Estação'] = 'Primavera'
    semente_jasmim_azul.to_csv('docs_bronze/lavoura_semente_jasmim_azul.csv')
    semente_morango = lista[35][0]
    semente_morango['Estação'] = 'Primavera'
    semente_morango.to_csv('docs_bronze/lavoura_semente_morango.csv')
    semente_rubiarmo = lista[39][0]
    semente_rubiarmo['Estação'] = 'Primavera'
    semente_rubiarmo.to_csv('docs_bronze/lavoura_semente_rubiarmo.csv')
    semente_tulipa = lista[42][0]
    semente_tulipa['Estação'] = 'Primavera' 
    semente_tulipa.to_csv('docs_bronze/lavoura_semente_tulipa.csv')
    muda_feijão = lista[46][0]
    muda_feijão['Estação'] = 'Primavera'
    muda_feijão.to_csv('docs_bronze/lavoura_muda_feijao.csv')
    #verão
    semente_carambola = lista[50][0]
    semente_carambola['Estação'] = 'Verão'
    semente_carambola.to_csv('docs_bronze/lavoura_semente_carambola.csv')
    semente_micanga = lista[54][0]
    semente_micanga['Estação'] = 'Verão'
    semente_micanga.to_csv('docs_bronze/lavoura_semente_micanga.csv')
    semente_girassol = lista[58][0]
    semente_girassol['Estação'] = 'Verão'
    semente_girassol.to_csv('docs_bronze/lavoura_semente_girassol.csv')
    muda_lupulo = lista[62][0]
    muda_lupulo['Estação'] = 'Verão'
    muda_lupulo.to_csv('docs_bronze/lavoura_muda_lupulo.csv')
    semente_melao = lista[66][0]
    semente_melao['Estação'] = 'Verão'
    semente_melao.to_csv('docs_bronze/lavoura_semente_melao.csv')
    semente_milho = lista[70][0]
    semente_milho['Estação'] = 'Verão'
    semente_milho.to_csv('docs_bronze/lavoura_semente_milho.csv')
    semente_mirtilo = lista[74][0]
    semente_mirtilo['Estação'] = 'Verão'
    semente_mirtilo.to_csv('docs_bronze/lavoura_semente_mirtilo.csv')
    semente_papoula = lista[78][0]
    semente_papoula['Estação'] = 'Verão'
    semente_papoula.to_csv('docs_bronze/lavoura_semente_papoula.csv')
    semente_pimenta = lista[82][0]
    semente_pimenta['Estação'] = 'Verão'
    semente_pimenta.to_csv('docs_bronze/lavoura_semente_pimenta.csv')
    semente_rabanete = lista[86][0]
    semente_rabanete['Estação'] = 'Verão'
    semente_rabanete.to_csv('docs_bronze/lavoura_semente_rabanete.csv')
    semente_repolho = lista[90][0]
    semente_repolho['Estação'] = 'Verão'
    semente_repolho.to_csv('docs_bronze/lavoura_semente_repolho.csv')
    semente_tomate = lista[94][0]
    semente_tomate['Estação'] = 'Verão'
    semente_tomate.to_csv('docs_bronze/lavoura_semente_tomate.csv')
    semente_trigo = lista[98][0]
    semente_trigo['Estação'] = 'Verão'
    semente_trigo.to_csv('docs_bronze/lavoura_semente_trigo.csv')
    #outono
    semente_abobora = lista[101][0]
    semente_abobora['Estação'] = 'Outono'
    semente_abobora.to_csv('docs_bronze/lavoura_semente_abobora.csv')
    semente_alcachofra = lista[104][0]
    semente_alcachofra['Estação'] = 'Outono'
    semente_alcachofra.to_csv('docs_bronze/lavoura_semente_alcachofra.csv')
    semente_amaranto = lista[108][0]
    semente_amaranto['Estação'] = 'Outono'
    semente_amaranto.to_csv('docs_bronze/lavoura_semente_amaranto.csv')
    semente_berinjela = lista[112][0]
    semente_berinjela['Estação'] = 'Outono'
    semente_berinjela.to_csv('docs_bronze/lavoura_semente_berinjela.csv')
    semente_beterraba = lista[116][0]
    semente_beterraba['Estação'] = 'Outono'
    semente_beterraba.to_csv('docs_bronze/lavoura_semente_beterraba.csv')
    semente_couve_chinesa = lista[120][0]
    semente_couve_chinesa['Estação'] = 'Outono'
    semente_couve_chinesa.to_csv('docs_bronze/lavoura_semente_couve_chinesa.csv')
    semente_inhame = lista[124][0]
    semente_inhame['Estação'] = 'Outono'
    semente_inhame.to_csv('docs_bronze/lavoura_semente_inhame.csv')
    semente_oxicoco = lista[128][0]
    semente_oxicoco['Estação'] = 'Outono'
    semente_oxicoco.to_csv('docs_bronze/lavoura_semente_oxicoco.csv')
    semente_fada = lista[132][0]
    semente_fada['Estação'] = 'Outono'
    semente_fada.to_csv('docs_bronze/lavoura_semente_fada.csv')
    muda_uva = lista[136][0]
    muda_uva['Estação'] = 'Outono'
    muda_uva.to_csv('docs_bronze/lavoura_muda_uva.csv')
    # especial
    semente_rara = lista[140][0]
    semente_rara['Estação'] = 'Especial'
    semente_rara.to_csv('docs_bronze/lavoura_semente_rara.csv')
    semente_antiga = lista[142][0]
    semente_antiga['Estação'] = 'Especial'
    semente_antiga.to_csv('docs_bronze/lavoura_semente_antiga.csv')
    semente_cacto = lista[144][0]
    semente_cacto['Estação'] = 'Especial'
    semente_cacto.to_csv('docs_bronze/lavoura_semente_cacto.csv')
    semente_abacaxi = lista[147][0]
    semente_abacaxi['Estação'] = 'Especial'
    semente_abacaxi.to_csv('docs_bronze/lavoura_semente_abacaxi.csv')
    broto_cha = lista[150][0]
    broto_cha['Estação'] = 'Especial'
    broto_cha.to_csv('docs_bronze/lavoura_broto_cha.csv')
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
    for lavoura in lista_lavouras:
        df = pd.read_csv(f'docs_bronze/lavoura_{lavoura}.csv')
        df = df.drop(columns=['Unnamed: 0'])
        df.loc[0, 'Semente'] = df.loc[0, 'Sementes'].split('  ')[0]
        df.loc[0, 'Origem'] = '  '.join(df.loc[0, 'Sementes'].split('  ')[1:])
        # pegar última linha de 'Vende por'
        df['Renda média (ouro por dia)'] = extrair_valor_ouro(df.iloc[-1])
        #preenche espaços em branco pela última linha
        df.iloc[0,:] = df.iloc[0,:].fillna(df.iloc[-1,:])
        #df = df.iloc[0,:]
        df.to_csv(f'docs_bronze/lavoura_{lavoura}.csv', index=False)

def df_animais(html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

    galinha = lista[0][0]
    galinha.to_csv('docs_bronze/animais_galinha.csv')
    pato = lista[1][0]
    pato.to_csv('docs_bronze/animais_pato.csv')
    coelho = lista[2][0]
    coelho.to_csv('docs_bronze/animais_coelho.csv')
    dinossauro = lista[3][0]
    dinossauro.to_csv('docs_bronze/animais_dinossauro.csv')
    vaca = lista[4][0]
    vaca.to_csv('docs_bronze/animais_vaca.csv')
    cabra = lista[5][0]
    cabra.to_csv('docs_bronze/animais_cabra.csv')
    ovelha = lista[6][0]
    ovelha.to_csv('docs_bronze/animais_ovelha.csv')
    porco = lista[7][0]
    porco.to_csv('docs_bronze/animais_porco.csv')
    avestruz = lista[8][0]
    avestruz.to_csv('docs_bronze/animais_avestruz.csv')

def df_arvores_frutiferas(html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv
    
    damasqueiro = lista[0][0]
    damasqueiro.to_csv('docs_bronze/arvores_damasqueiro.csv')
    muda_damasqueiro = lista[1][0]
    muda_damasqueiro.to_csv('docs_bronze/arvores_muda_damasqueiro.csv')
    cerejeira = lista[4][0]
    cerejeira.to_csv('docs_bronze/arvores_cerejeira.csv')
    muda_cerejeira = lista[5][0]
    muda_cerejeira.to_csv('docs_bronze/arvores_muda_cerejeira.csv')
    laranjeira = lista[8][0]
    laranjeira.to_csv('docs_bronze/arvores_laranjeira.csv')
    muda_laranjeira = lista[9][0]
    muda_laranjeira.to_csv('docs_bronze/arvores_muda_laranjeira.csv')
    pessegueira = lista[12][0]
    pessegueira.to_csv('docs_bronze/arvores_pessegueira.csv')
    muda_pessegueira = lista[13][0]
    muda_pessegueira.to_csv('docs_bronze/arvores_muda_pessegueira.csv')
    bananeira = lista[16][0]
    bananeira.to_csv('docs_bronze/arvores_bananeira.csv')
    muda_bananeira = lista[17][0]
    muda_bananeira.to_csv('docs_bronze/arvores_muda_bananeira.csv')
    mangueira = lista[20][0]
    mangueira.to_csv('docs_bronze/arvores_mangueira.csv')
    muda_mangueira = lista[21][0]
    muda_mangueira.to_csv('docs_bronze/arvores_muda_mangueira.csv')
    macieira = lista[24][0]
    macieira.to_csv('docs_bronze/arvores_macieira.csv')
    muda_macieira = lista[25][0]
    muda_macieira.to_csv('docs_bronze/arvores_muda_macieira.csv')
    romanzeira = lista[28][0]
    romanzeira.to_csv('docs_bronze/arvores_romanzeira.csv')
    muda_romanzeira = lista[29][0]
    muda_romanzeira.to_csv('docs_bronze/arvores_muda_romanzeira.csv')

def df_mercadorias_artesanais(html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

    apiario = lista[0][0]
    apiario.to_csv('docs_bronze/mercadoria_apiario.csv')
    mel = lista[1][0]
    mel.to_csv('docs_bronze/mercadoria_mel.csv')
    barril_madeira = lista[2][0]
    barril_madeira.to_csv('docs_bronze/mercadoria_barril_madeira.csv')
    produto_barril_madeira = lista[3][0]
    produto_barril_madeira.to_csv('docs_bronze/mercadoria_produto_barril_madeira.csv')
    prensa_queijo = lista[28][0]
    prensa_queijo.to_csv('docs_bronze/mercadoria_prensa_queijo.csv')
    produto_prensa_queijo = lista[29][0]
    produto_prensa_queijo.to_csv('docs_bronze/mercadoria_produto_prensa_queijo.csv')
    barril = lista[34][0]
    barril.to_csv('docs_bronze/mercadoria_barril.csv')
    produto_barril = lista[35][0]
    produto_barril.to_csv('docs_bronze/mercadoria_produto_barril.csv')
    tear = lista[36][0]
    tear.to_csv('docs_bronze/mercadoria_tear.csv')
    produto_tear = lista[37][0]
    produto_tear.to_csv('docs_bronze/mercadoria_produto_tear.csv')
    maquina_maionese = lista[38][0]
    maquina_maionese.to_csv('docs_bronze/mercadoria_maquina_maionese.csv')
    produto_maquina_maionese = lista[39][0]
    produto_maquina_maionese.to_csv('docs_bronze/mercadoria_produto_maquina_maionese.csv')
    maquina_molho = lista[40][0]
    maquina_molho.to_csv('docs_bronze/mercadoria_maquina_molho.csv')
    produto_maquina_molho = lista[41][0]
    produto_maquina_molho.to_csv('docs_bronze/mercadoria_produto_maquina_molho.csv')
    gerador_oleo = lista[44][0]
    gerador_oleo.to_csv('docs_bronze/mercadoria_gerador_oleo.csv')
    produto_gerador_oleo = lista[45][0]
    produto_gerador_oleo.to_csv('docs_bronze/mercadoria_produto_gerador_oleo.csv')
    jarra_conserva = lista[46][0]
    jarra_conserva.to_csv('docs_bronze/mercadoria_jarra_conserva.csv')
    produto_jarra_conserva = lista[47][0]
    produto_jarra_conserva.to_csv('docs_bronze/mercadoria_produto_jarra_conserva.csv')

def df_casa_fazenda(html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

    casa_estagios = lista[1][0]
    casa_estagios.to_csv('docs_bronze/casa_estagios.csv')
    casa_renovacooes = lista[3][0]
    casa_renovacooes.to_csv('docs_bronze/casa_renovacoes.csv')

def df_caverna(html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

    caverna_morcego = lista[0][0]
    caverna_morcego.to_csv('docs_bronze/caverna_morcego.csv')
    caverna_cogumelo = lista[21][0]
    caverna_cogumelo.to_csv('docs_bronze/caverna_cogumelo.csv')

def df_estufa(html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

    estufa = lista[0][0]
    estufa.to_csv('docs_bronze/casa_estufa.csv')

    pass

def df_casa(html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

    #sem tabela

def df_clima(html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

    clima = lista[1][0]        
    clima.to_csv('docs_bronze/clima.csv')

def df_caverna(html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

def df_primavera(html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv
    calendario_primavera_festivais = lista[1][0]
    calendario_primavera_festivais.to_csv('docs_bronze/calendario_primavera_festivais.csv')
    calendario_primavera_aniversario = lista[2][0]
    calendario_primavera_aniversario.to_csv('docs_bronze/calendario_primavera_aniversario.csv')
    calendario_primavera_colheita_unica = lista[4][0]
    calendario_primavera_colheita_unica.to_csv('docs_bronze/calendario_primavera_colheita_unica.csv')
    calendario_primavera_colheita_multipla = lista[5][0]
    calendario_primavera_colheita_multipla.to_csv('docs_bronze/calendario_primavera_colheita_multipla.csv')
    calendario_primavera_pesca = lista[23][0]
    calendario_primavera_pesca.to_csv('docs_bronze/calendario_primavera_pesca.csv')

def df_verao(html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

    calendario_verao_festivais = lista[1][0]
    calendario_verao_festivais.to_csv('docs_bronze/calendario_verao_festivais.csv')
    calendario_verao_aniversario = lista[2][0]
    calendario_verao_aniversario.to_csv('docs_bronze/calendario_verao_aniversario.csv')
    calendario_verao_colheita_unica = lista[3][0]
    calendario_verao_colheita_unica.to_csv('docs_bronze/calendario_verao_colheita_unica.csv')
    calendario_verao_colheita_multipla = lista[4][0]
    calendario_verao_colheita_multipla.to_csv('docs_bronze/calendario_verao_colheita_multipla.csv')
    calendario_verao_pesca = lista[16][0]
    calendario_verao_pesca.to_csv('docs_bronze/calendario_verao_pesca.csv')

def df_outono(html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

    calendario_outono_festivais = lista[1][0]
    calendario_outono_festivais.to_csv('docs_bronze/calendario_outono_festivais.csv')
    calendario_outono_aniversario = lista[2][0]
    calendario_outono_aniversario.to_csv('docs_bronze/calendario_outono_aniversario.csv')
    calendario_outono_colheita_unica = lista[3][0]
    calendario_outono_colheita_unica.to_csv('docs_bronze/calendario_outono_colheita_unica.csv')
    calendario_outono_colheita_multipla = lista[5][0]
    calendario_outono_colheita_multipla.to_csv('docs_bronze/calendario_outono_colheita_multipla.csv')
    calendario_outono_pesca = lista[19][0]
    calendario_outono_pesca.to_csv('docs_bronze/calendario_outono_pesca.csv')

def df_inverno(html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

    calendario_inverno_festivais = lista[2][0]
    calendario_inverno_festivais.to_csv('docs_bronze/calendario_inverno_festivais.csv')
    calendario_inverno_aniversario = lista[3][0]
    calendario_inverno_aniversario.to_csv('docs_bronze/calendario_inverno_aniversario.csv')
    calendario_inverno_colheita = lista[4][0]
    calendario_inverno_colheita.to_csv('docs_bronze/calendario_inverno_colheita.csv')
    calendario_inverno_pesca = lista[23][0]
    calendario_inverno_pesca.to_csv('docs_bronze/calendario_inverno_pesca.csv')

def df_missoes(html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

    missoes = lista[0][0]
    missoes.to_csv('docs_bronze/missoes.csv')
    missoes_lista = lista[1][0]
    missoes_lista.to_csv('docs_bronze/missoes_lista.csv')
    missoes_itens_lista = lista[2][0]
    missoes_itens_lista.to_csv('docs_bronze/missoes_itens_lista.csv')
    missoes_pedidos_especiais = lista[3][0]
    missoes_pedidos_especiais.to_csv('docs_bronze/missoes_pedidos_especiais.csv')
    missoes_pedidos_especiais_sr_qi = lista[4][0]
    missoes_pedidos_especiais_sr_qi.to_csv('docs_bronze/missoes_especiais_sr_qi.csv')

def df_conjuntos(html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table', class_= 'wikitable'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

    conjunto_primavera = lista[1][0]
    conjunto_primavera.to_csv('docs_bronze/conjunto_primavera.csv')
    conjunto_verao = lista[2][0]
    conjunto_verao.to_csv('docs_bronze/conjunto_verao.csv')
    conjunto_outono = lista[3][0]
    conjunto_outono.to_csv('docs_bronze/conjunto_outono.csv')
    conjunto_inverno = lista[4][0]
    conjunto_inverno.to_csv('docs_bronze/conjunto_inverno.csv')
    conjunto_construcao = lista[5][0]
    conjunto_construcao.to_csv('docs_bronze/conjunto_construcao.csv')
    conjunto_recursos_exoticos = lista[6][0]
    conjunto_recursos_exoticos.to_csv('docs_bronze/conjunto_recursos_exoticos.csv')
    conjunto_plantacoes_primavera = lista[8][0]
    conjunto_plantacoes_primavera.to_csv('docs_bronze/conjunto_plantacoes_primavera.csv')
    conjunto_plantacoes_verao = lista[9][0]
    conjunto_plantacoes_verao.to_csv('docs_bronze/conjunto_plantacoes_verao.csv')
    conjunto_plantacoes_outono = lista[10][0]
    conjunto_plantacoes_outono.to_csv('docs_bronze/conjunto_plantacoes_outono.csv')
    conjunto_plantacoes_qualidade = lista[11][0]
    conjunto_plantacoes_qualidade.to_csv('docs_bronze/conjunto_plantacoes_qualidade.csv')
    conjunto_animal = lista[12][0]
    conjunto_animal.to_csv('docs_bronze/conjunto_animal.csv')
    conjunto_artesao = lista[13][0]
    conjunto_artesao.to_csv('docs_bronze/conjunto_artesao.csv')
    conjunto_peixes_rio = lista[15][0]
    conjunto_peixes_rio.to_csv('docs_bronze/conjunto_peixes_rio.csv')
    conjunto_peixes_lago = lista[16][0]
    conjunto_peixes_lago.to_csv('docs_bronze/conjunto_peixes_lago.csv')
    conjunto_peixes_oceano = lista[17][0]
    conjunto_peixes_oceano.to_csv('docs_bronze/conjunto_peixes_oceano.csv')
    conjunto_pesca_noturna = lista[18][0]
    conjunto_pesca_noturna.to_csv('docs_bronze/conjunto_pesca_noturna.csv')
    conjunto_pesca_covo = lista[19][0]
    conjunto_pesca_covo.to_csv('docs_bronze/conjunto_pesca_covo.csv')
    conjunto_peixes_especializados = lista[20][0]
    conjunto_peixes_especializados.to_csv('docs_bronze/conjunto_peixes_especializados.csv')
    conjunto_ferreiro = lista[22][0]
    conjunto_ferreiro.to_csv('docs_bronze/conjunto_ferreiro.csv')
    conjunto_geologo = lista[23][0]
    conjunto_geologo.to_csv('docs_bronze/conjunto_geologo.csv')
    conjunto_aventureiro = lista[24][0]
    conjunto_aventureiro.to_csv('docs_bronze/conjunto_aventureiro.csv')
    conjunto_cozinheiro = lista[26][0]
    conjunto_cozinheiro.to_csv('docs_bronze/conjunto_cozinheiro.csv')
    conjunto_tinta = lista[27][0]
    conjunto_tinta.to_csv('docs_bronze/conjunto_tinta.csv')
    conjunto_pesquisa_campo = lista[28][0]
    conjunto_pesquisa_campo.to_csv('docs_bronze/conjunto_pesquisa_campo.csv')
    conjunto_forragem = lista[29][0]
    conjunto_forragem.to_csv('docs_bronze/conjunto_forragem.csv')
    conjunto_encantador = lista[30][0]
    conjunto_encantador.to_csv('docs_bronze/conjunto_encantador.csv')
    conjunto_2500 = lista[32][0]
    conjunto_2500.to_csv('docs_bronze/conjunto_2500.csv')
    conjunto_5000 = lista[33][0]
    conjunto_5000.to_csv('docs_bronze/conjunto_5000.csv')
    conjunto_10000 = lista[34][0]
    conjunto_10000.to_csv('docs_bronze/conjunto_10000.csv')
    conjunto_25000 = lista[35][0]
    conjunto_25000.to_csv('docs_bronze/conjunto_25000.csv')
    conjunto_a_desaparecida = lista[37][0]
    conjunto_a_desaparecida.to_csv('docs_bronze/conjunto_a_desaparecida.csv')

    pass

def df_conquistas (html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

    conquistas = lista[0][0]
    conquistas.to_csv('docs_bronze/conquistas.csv')

    pass

def df_ferramentas (html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela))))
    efeitos = lista[0][0]
    efeitos.to_csv('docs_bronze/ferramenta_efeitos.csv')
    enxada = lista[1][0]
    enxada.to_csv('docs_bronze/ferramenta_enxada.csv')
    picareta = lista[2][0]
    picareta.to_csv('docs_bronze/ferramenta_picareta.csv')
    machado = lista[3][0]
    machado.to_csv('docs_bronze/ferramenta_machado.csv')
    regador = lista[4][0]
    regador.to_csv('docs_bronze/ferramenta_regador.csv')
    lixeira = lista[5][0]
    lixeira.to_csv('docs_bronze/ferramenta_lixeira.csv')
    vara_pesca = lista[6][0]
    vara_pesca.to_csv('docs_bronze/ferramenta_vara_pesca.csv')
    foice = lista[7][0]
    foice.to_csv('docs_bronze/ferramenta_foice.csv')

    

def df_armas (html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

    luta_atributos = lista[1][0]
    luta_atributos.to_csv('docs_bronze/armas_luta_atributos.csv')
    espadas = lista[2][0]
    espadas.to_csv('docs_bronze/armas_espadas.csv')
    adagas = lista[3][0]
    adagas.to_csv('docs_bronze/armas_adagas.csv')
    clavas= lista[4][0]
    clavas.to_csv('docs_bronze/armas_clavas.csv')
    estilingues = lista[5][0]
    estilingues.to_csv('docs_bronze/armas_estilingues.csv')
    municoes =lista[6][0]
    municoes.to_csv('docs_bronze/armas_municoes.csv')
    armas_impossiveis = lista[7][0]
    armas_impossiveis.to_csv('docs_bronze/armas_impossiveis.csv')

    pass

def df_chapeus (html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

    chapeus = lista[0][0]
    chapeus.to_csv('docs_bronze/chapeus.csv')

    pass

def df_calcados (html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

    calcados = lista[0][0]
    calcados.to_csv('docs_bronze/calcados.csv')

    pass

def df_aneis (html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

    aneis = lista[0][0]
    aneis.to_csv('docs_bronze/aneis.csv')

    pass

def df_chapeus (html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

    chapeus = lista[0][0]
    chapeus.to_csv('docs_bronze/chapeus.csv')

    pass

def df_peixes (html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

    peixes_vara_pesca = lista[0][0]
    peixes_vara_pesca.to_csv('docs_bronze/peixes_vara_pesca.csv')
    peixes_mercado_noturno = lista[145][0]
    peixes_mercado_noturno.to_csv('docs_bronze/peixes_mercado_noturno.csv')
    peixes_lendarios = lista[155][0]
    peixes_lendarios.to_csv('docs_bronze/peixes_lendarios.csv')
    peixes_lendarios_ii = lista[171][0]
    peixes_lendarios_ii.to_csv('docs_bronze/peixes_lendarios_ii.csv')
    peixes_covo = lista[187][0]
    peixes_covo.to_csv('docs_bronze/peixes_covo.csv')
    itens_pescaveis = lista[198][0]
    itens_pescaveis.to_csv('docs_bronze/peixes_itens_pescaveis.csv')
    receitas_pesca = lista[200][0]
    receitas_pesca.to_csv('docs_bronze/peixes_receitas_pesca.csv')
    peixe_sashimi = lista[202][0]
    peixe_sashimi.to_csv('docs_bronze/peixes_sashimi.csv')

    pass

def df_iscas (html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

    iscas = lista[0][0]
    iscas.to_csv('docs_bronze/iscas.csv')

    pass

def df_fertilizantes (html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

    fertilizante = lista[0][0]
    fertilizante.to_csv('docs_bronze/fertilizante.csv')
    taxa_cultivo_solo_normal = lista[1][0]
    taxa_cultivo_solo_normal.to_csv('docs_bronze/taxa_cultivo_solo_normal.csv')
    taxa_cultivo_fertilizante_basico = lista[2][0]
    taxa_cultivo_fertilizante_basico.to_csv('docs_bronze/taxa_cultivo_fertilizante_basico.csv')
    taxa_cultivo_fertilizante_qualidade = lista[3][0]
    taxa_cultivo_fertilizante_qualidade.to_csv('docs_bronze/taxa_cultivo_fertilizante_qualidade.csv')
    taxa_cultivo_fertilizante_premium = lista[4][0]
    taxa_cultivo_fertilizante_premium.to_csv('docs_bronze/taxa_cultivo_fertilizante_premium.csv')
    custo_solo_foliar_concha = lista[6][0]
    custo_solo_foliar_concha.to_csv('docs_bronze/custo_solo_foliar_concha.csv')
    custo_solo_foliar_coral = lista[8][0]
    custo_solo_foliar_coral.to_csv('docs_bronze/custo_solo_foliar_coral.csv')

    pass

def df_culinaria (html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

    culinaria_receitas = lista[3][0]
    culinaria_receitas.to_csv('docs_bronze/culinaria_receitas.csv')
    culinaria_cultivos = lista[36][0]
    culinaria_cultivos.to_csv('docs_bronze/culinaria_cultivos.csv')
    culinaria_itens_coleta = lista[37][0]
    culinaria_itens_coleta.to_csv('docs_bronze/culinaria_itens_coleta.csv')
    culinaria_frutas_arvore = lista[38][0]
    culinaria_frutas_arvore.to_csv('docs_bronze/culinaria_frutas_arvore.csv')
    culinaria_produtos_animais = lista[39][0]
    culinaria_produtos_animais.to_csv('docs_bronze/culinaria_produtos_naturais.csv')
    culinaria_mercadorias_artesanais = lista[40][0]
    culinaria_mercadorias_artesanais.to_csv('docs_bronze/culinaria_mercadorias_artesanais.csv')
    culinaria_diversos = lista[41][0]
    culinaria_diversos.to_csv('docs_bronze/culinaria_diversos.csv')
    culinaria_pescaria = lista[42][0]
    culinaria_pescaria.to_csv('docs_bronze/culinaria_pescaria.csv')
    culinaria_covo = lista[43][0]
    culinaria_covo.to_csv('docs_bronze/culinaria_covo.csv')
    culinaria_itens_loja = lista[44][0]
    culinaria_itens_loja.to_csv('docs_bronze/culinaria_itens_loja.csv')
    culinaria_pratos_ingredientes = lista[45][0]
    culinaria_pratos_ingredientes.to_csv('docs_bronze/culinaria_pratos_ingredientes.csv')

    pass

def df_artesanato (html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

    artesanato_bombas = lista[0][0]
    artesanato_bombas.to_csv('docs_bronze/artesanato_bombas.csv')
    artesanato_cercas = lista[1][0]
    artesanato_cercas.to_csv('docs_bronze/artesanato_cercas.csv')
    artesanato_aspersores = lista[2][0]
    artesanato_aspersores.to_csv('docs_bronze/artesanato_aspersores.csv')
    artesanato_equipamentos_artesanais = lista[3][0]
    artesanato_equipamentos_artesanais.to_csv('docs_bronze/artesanato_equipamentos_artesanais.csv')
    artesanato_fertilizantes = lista[4][0]
    artesanato_fertilizantes.to_csv('docs_bronze/artesanato_fertilizantes.csv')
    artesanato_sementes = lista[5][0]
    artesanato_sementes.to_csv('docs_bronze/artesanato_sementes.csv')
    artesanato_decoracao = lista[6][0]
    artesanato_decoracao.to_csv('docs_bronze/artesanato_decoracao.csv')
    artesanato_pesca = lista[7][0]
    artesanato_pesca.to_csv('docs_bronze/artesanato_pesca.csv')
    artesanato_aneis = lista[8][0]
    artesanato_aneis.to_csv('docs_bronze/artesanato_aneis.csv')
    artesanato_itens_comestiveis = lista[9][0]
    artesanato_itens_comestiveis.to_csv('docs_bronze/artesanato_itens_comestiveis.csv')
    artesanato_iluminacao = lista[10][0]
    artesanato_iluminacao.to_csv('docs_bronze/artesanato_iluminacao.csv')
    artesanato_equipamento_refino = lista[11][0]
    artesanato_equipamento_refino.to_csv('docs_bronze/artesanato_equipamento_refino.csv')
    artesanato_mobilia = lista[12][0]
    artesanato_mobilia.to_csv('docs_bronze/artesanato_mobilia.csv')
    artesanato_diversos = lista[13][0]
    artesanato_diversos.to_csv('docs_bronze/artesanato_diversos.csv')

    pass

def df_carteira (html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv
    
    carteira_itens_especiais = lista[1][0]
    carteira_itens_especiais.to_csv('docs_bronze/carteira_itens_especiais.csv')
    livros_poderes_especiais = lista[2][0]
    livros_poderes_especiais.to_csv('docs_bronze/carteira_livros_poderes_especiais.csv')
    poderes_maestria = lista[3][0]
    poderes_maestria.to_csv('docs_bronze/carteira_poderes_maestria.csv')

    pass

def df_artefatos(html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv
    
    artefatos = lista[0][0]
    artefatos.to_csv('docs_bronze/artefatos.csv')
    artefatos_tesouro = lista[1][0]
    artefatos_tesouro.to_csv('docs_bronze/artefatos_tesouro.csv')

    pass

def df_minerais(html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

    minerais_coleta = lista[0][0]
    minerais_coleta.to_csv('docs_bronze/minerais_coleta.csv')
    minerais_gemas = lista[1][0]
    minerais_gemas.to_csv('docs_bronze/minerais_gemas.csv')
    minerais_origem_geodos = lista[2][0]
    minerais_origem_geodos.to_csv('docs_bronze/minerais_origem_geodos.csv')
    geodos = lista[3][0]
    geodos.to_csv('docs_bronze/minerais_geodos.csv')

    pass

def df_mobilia(html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv

    sofas = lista[1][0]
    sofas.to_csv('docs_bronze/mobilia_sofas.csv')
    poltronas = lista[2][0]
    poltronas.to_csv('docs_bronze/mobilia_poltronas.csv')
    cadeiras1 = lista[4][0]
    cadeiras1.to_csv('docs_bronze/mobilia_cadeiras1.csv')
    cadeiras2 = lista[5][0]
    cadeiras2.to_csv('docs_bronze/mobilia_cadeiras2.csv')
    cadeiras3 = lista[6][0]
    cadeiras3.to_csv('docs_bronze/mobilia_cadeiras3.csv')
    bancos = lista[7][0]
    bancos.to_csv('docs_bronze/mobilia_bancos.csv')
    mesas1 = lista[9][0]
    mesas1.to_csv('docs_bronze/mobilia_mesas1.csv')
    mesas2 = lista[10][0]
    mesas2.to_csv('docs_bronze/mobilia_mesas2.csv')
    mesas3 = lista[11][0]
    mesas3.to_csv('docs_bronze/mobilia_mesas3.csv')
    mesas_longas = lista[12][0]
    mesas_longas.to_csv('docs_bronze/mobilia_mesas_longas.csv')
    estantes = lista[14][0]
    estantes.to_csv('docs_bronze/mobilia_estantes.csv')
    comodas = lista[15][0]
    comodas.to_csv('docs_bronze/mobilia_comodas.csv')
    lareiras = lista[16][0]
    lareiras.to_csv('docs_bronze/mobilia_lareiras.csv')
    tapetes = lista[17][0]
    tapetes.to_csv('docs_bronze/mobilia_tapetes.csv')
    lampadas = lista[20][0]
    lampadas.to_csv('docs_bronze/mobilia_lampadas.csv')
    janelas = lista[21][0]
    janelas.to_csv('docs_bronze/mobilia_janelas.csv')
    tvs = lista[22][0]
    tvs.to_csv('docs_bronze/mobilia_tvs.csv')
    camas = lista[23][0]
    camas.to_csv('docs_bronze/mobilia_camas.csv')
    plantas_decorativas_chao1 = lista[26][0]
    plantas_decorativas_chao1.to_csv('docs_bronze/mobilia_plantas_decorativas_chao1.csv')
    plantas_decorativas_chao2 = lista[27][0]
    plantas_decorativas_chao2.to_csv('docs_bronze/mobilia_plantas_decorativas_chao2.csv')
    plantas_decorativas_penduradas = lista[28][0]
    plantas_decorativas_penduradas.to_csv('docs_bronze/mobilia_plantas_decorativas_penduradas.csv')
    plantas_decorativas_sazonais = lista[29][0]
    plantas_decorativas_sazonais.to_csv('docs_bronze/mobilia_plantas_decorativas_sazonais.csv')
    pinturas = lista[30][0]
    pinturas.to_csv('docs_bronze/mobilia_pinturas.csv')
    pinturas_mercado_noturno = lista[32][0]
    pinturas_mercado_noturno.to_csv('docs_bronze/mobilia_pinturas_mercado_noturno.csv')
    posteres = lista[34][0]
    posteres.to_csv('docs_bronze/mobilia_posteres.csv')
    bandeiras = lista[36][0]
    bandeiras.to_csv('docs_bronze/mobilia_bandeiras.csv')
    decoracao_parede = lista[38][0]
    decoracao_parede.to_csv('docs_bronze/mobilia_decoracao_parede.csv')
    decoracao_parede2 = lista[39][0]
    decoracao_parede2.to_csv('docs_bronze/mobilia_decoracao_parede2.csv')
    aquarios = lista[40][1]
    aquarios.to_csv('docs_bronze/mobilia_aquarios.csv')
    tochas = lista[40][2]
    tochas.to_csv('docs_bronze/mobilia_tochas.csv')
    mobilia_diversos1 = lista[40][4]
    mobilia_diversos1.to_csv('docs_bronze/mobilia_diversos1.csv')
    mobilia_diversos2 = lista[40][5]
    mobilia_diversos2.to_csv('docs_bronze/mobilia_diversos2.csv')
    mobilia_outras_decoracoes1 = lista[40][7]
    mobilia_outras_decoracoes1.to_csv('docs_bronze/mobilia_outras_decoracoes1.csv')
    mobilia_outras_decoracoes2 = lista[40][8]
    mobilia_outras_decoracoes2.to_csv('docs_bronze/mobilia_outras_decoracoes2.csv')
    mobilia_itens_especiais1 = lista[40][10]
    mobilia_itens_especiais1.to_csv('docs_bronze/mobilia_itens_especiais1.csv')
    mobilia_itens_especiais2 = lista[40][11]
    mobilia_itens_especiais2.to_csv('docs_bronze/mobilia_itens_especiais2.csv')
    mobilia_catalogo = lista[40][12]
    mobilia_catalogo.to_csv('docs_bronze/mobilia_catalogo.csv')

    pass

def df_presentes_favoritos (html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv
    
    lista_presentes = lista[0][0]
    lista_presentes.to_csv('docs_bronze/lista_presentes.csv')

def df_construcoes_fazenda (html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    sopa = bs4(html, 'html.parser')
    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv
    """for i in range(len(lista)):
        for j in range(len(lista[i])):
            print(f'i = {i}, j = {j}')
            print(lista[i][j])
        print('*-* FIM DA TABELA *-*'*5) """
    loja_carpintaria = lista[0][0]
    loja_carpintaria.to_csv('docs_bronze/loja_carpintaria.csv')
    estoque_carpintaria_permanente = lista[1][0]
    estoque_carpintaria_permanente.to_csv('docs_bronze/estoque_carpintaria_permanente.csv')
    estoque_carpintaria_rotativo = lista[3][0]
    estoque_carpintaria_rotativo.to_csv('docs_bronze/estoque_carpintaria_rotativo.csv')
    construcoes_fazenda_carpintaria = lista[4][0]
    construcoes_fazenda_carpintaria.to_csv('docs_bronze/casa_construcoes_fazenda.csv')
    construcoes_fazenda_carpintaria_melhoria = lista[5][0]
    construcoes_fazenda_carpintaria_melhoria.to_csv('docs_bronze/casa_construcoes_melhoria.csv')
    construcoes_fazenda_carpintaria_renovacoes = lista[6][0]
    construcoes_fazenda_carpintaria_renovacoes.to_csv('docs_bronze/casa_construcoes_renovacoes.csv')

if __name__ == '__main__':
    #import
    from bs4 import BeautifulSoup as bs4
    import pandas as pd
    from io import StringIO

    #execute
    df_cultivo(html='docs_raw/sopa_Cultivo.html')
    df_mineracao(html='docs_raw/sopa_Mineração.html')
    df_coleta(html='docs_raw/sopa_Coleta.html')
    df_pesca(html='docs_raw/sopa_Pesca.html')
    df_combate(html='docs_raw/sopa_Combate.html')
    df_lavouras(html='docs_raw/sopa_Lavouras.html')
    df_animais(html='docs_raw/sopa_Animais.html')
    df_arvores_frutiferas(html='docs_raw/sopa_Árvores_frutíferas.html')
    df_mercadorias_artesanais(html='docs_raw/sopa_Mercadorias_Artesanais.html')
    df_casa_fazenda(html='docs_raw/sopa_Casa_da_Fazenda.html')
    df_caverna(html='docs_raw/sopa_A_Caverna.html')
    df_estufa(html='docs_raw/sopa_Estufa.html')
    df_casa(html='docs_raw/sopa_Casa.html') #sem tabela
    df_clima(html='docs_raw/sopa_Clima.html')
    df_primavera(html='docs_raw/sopa_Primavera.html')
    df_verao(html='docs_raw/sopa_Verão.html')
    df_outono(html='docs_raw/sopa_Outono.html')
    df_inverno(html='docs_raw/sopa_Inverno.html')
    #'Festivais', #18
    #'Monstros', #19
    #'Televisão', #20
    #'Aldeões', #21
    #'Amizade', #22
    #'Casamento', #23
    #'Crianças', #24
    df_missoes(html='docs_raw/sopa_Missões.html')
    df_conjuntos(html='docs_raw/sopa_Conjuntos.html')
    df_conquistas(html='docs_raw/sopa_Conquistas.html')
    #'Modificações', #29
    df_ferramentas(html='docs_raw/sopa_ferramentas.html')
    df_armas(html='docs_raw/sopa_Armas.html')
    df_chapeus(html='docs_raw/sopa_Chapéus.html')
    df_calcados(html='docs_raw/sopa_Calçados.html')
    df_aneis(html='docs_raw/sopa_Anéis.html')
    df_peixes(html='docs_raw/sopa_Peixes.html')
    df_iscas(html='docs_raw/sopa_Isca.html')
    #'Anzóis', #37 # tem tabela
    df_fertilizantes(html='docs_raw/sopa_Fertilizante.html')
    df_culinaria(html='docs_raw/sopa_Culinária.html')
    df_artesanato(html='docs_raw/sopa_Artesanato.html')
    #'Árvores', #41
    #'Recados_Secretos', #42
    df_carteira(html='docs_raw/sopa_Carteira.html')
    df_artefatos(html='docs_raw/sopa_Artefatos.html')
    df_minerais(html='docs_raw/sopa_Minerais.html')
    df_mobilia(html='docs_raw/sopa_Mobília.html')
    #'Papel_de_Parede', #47
    #'Pisos', #48
    #'Vila_Pelicanos', #49
    df_presentes_favoritos(html='docs_raw\sopa_Lista_de_Todos_os_Presentes.html')
    #'Ferreiro', #51
    #'Mercado_Joja', #52
    #'Museu', #53,
    #'Armazém_do_Pierre', #54
    #'Saloon_Fruta_Estrelar', #55
    #'Rancho_da_Marnie', #56
    #'Casa_Arruinada', #57
    #'Bosque_Secreto', #58
    #'Torre_do_mago', #59
    #'Peixaria', #60
    #'A_Montanha', #61
    #'Guilda_dos_Aventureiros', #62
    df_construcoes_fazenda(html='docs_raw\sopa_Carpintaria.html')
