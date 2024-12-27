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

def df_lavouras(html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html = f.read()
    
    sopa = bs4(html, 'html.parser')

    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela)))) #só funciona se ativar .venv
    # primavera
    semente_alho = lista[1][0]
    semente_alho.to_csv('docs_bronze/lavoura_semente_alho.csv')
    semente_arroz = lista[5][0]
    semente_arroz.to_csv('docs_bronze/lavoura_semente_arroz.csv')
    semente_batata = lista[8][0]
    semente_batata.to_csv('docs_bronze/lavoura_semente_batata.csv')
    semente_cenoura = lista[12][0]
    semente_cenoura.to_csv('docs_bronze/lavoura_semente_cenoura.csv')
    semente_chirivia = lista[16][0]
    semente_chirivia.to_csv('docs_bronze/lavoura_semente_chirivia.csv')
    semente_couve = lista[20][0]
    semente_couve.to_csv('docs_bronze/lavoura_semente_couve.csv')
    semente_couve_flor = lista[24][0]
    semente_couve_flor.to_csv('docs_bronze/lavoura_semente_couve_flor.csv')
    grao_cafe = lista[28][0]
    grao_cafe.to_csv('docs_bronze/lavoura_grao_cafe.csv')
    semente_jasmim_azul = lista[31][0]
    semente_jasmim_azul.to_csv('docs_bronze/lavoura_semente_jasmim_azul.csv')
    semente_morango = lista[35][0]
    semente_morango.to_csv('docs_bronze/lavoura_semente_morango.csv')
    semente_rubiarmo = lista[39][0]
    semente_rubiarmo.to_csv('docs_bronze/lavoura_semente_rubiarmo.csv')
    semente_tulipa = lista[42][0]
    semente_tulipa.to_csv('docs_bronze/lavoura_semente_tulipa.csv')
    muda_feijão = lista[46][0]
    muda_feijão.to_csv('docs_bronze/lavoura_muda_feijao.csv')
    #verão
    semente_carambola = lista[50][0]
    semente_carambola.to_csv('docs_bronze/lavoura_semente_carambola.csv')
    semente_micanga = lista[54][0]
    semente_micanga.to_csv('docs_bronze/lavoura_semente_micanga.csv')
    semente_girassol = lista[58][0]
    semente_girassol.to_csv('docs_bronze/lavoura_semente_girassol.csv')
    muda_lupulo = lista[62][0]
    muda_lupulo.to_csv('docs_bronze/lavoura_muda_lupulo.csv')
    semente_melao = lista[66][0]
    semente_melao.to_csv('docs_bronze/lavoura_semente_melao.csv')
    semente_milho = lista[70][0]
    semente_milho.to_csv('docs_bronze/lavoura_semente_milho.csv')
    semente_mirtilo = lista[74][0]
    semente_mirtilo.to_csv('docs_bronze/lavoura_semente_mirtilo.csv')
    semente_papoula = lista[78][0]
    semente_papoula.to_csv('docs_bronze/lavoura_semente_papoula.csv')
    semente_pimenta = lista[82][0]
    semente_pimenta.to_csv('docs_bronze/lavoura_semente_pimenta.csv')
    semente_rabanete = lista[86][0]
    semente_rabanete.to_csv('docs_bronze/lavoura_semente_rabanete.csv')
    semente_repolho = lista[90][0]
    semente_repolho.to_csv('docs_bronze/lavoura_semente_repolho.csv')
    semente_tomate = lista[94][0]
    semente_tomate.to_csv('docs_bronze/lavoura_semente_tomate.csv')
    semente_trigo = lista[98][0]
    semente_trigo.to_csv('docs_bronze/lavoura_semente_trigo.csv')
    #outono
    semente_abobora = lista[101][0]
    semente_abobora.to_csv('docs_bronze/lavoura_semente_abobora.csv')
    semente_alcachofra = lista[104][0]
    semente_alcachofra.to_csv('docs_bronze/lavoura_semente_alcachofra.csv')
    semente_amaranto = lista[108][0]
    semente_amaranto.to_csv('docs_bronze/lavoura_semente_amaranto.csv')
    semente_beringela = lista[112][0]
    semente_beringela.to_csv('docs_bronze/lavoura_semente_beringela.csv')
    semente_beterraba = lista[116][0]
    semente_beterraba.to_csv('docs_bronze/lavoura_semente_beterraba.csv')
    semente_couve_chinesa = lista[120][0]
    semente_couve_chinesa.to_csv('docs_bronze/lavoura_semente_couve_chinesa.csv')
    semente_inhame = lista[124][0]
    semente_inhame.to_csv('docs_bronze/lavoura_semente_inhame.csv')
    semente_oxicoco = lista[128][0]
    semente_oxicoco.to_csv('docs_bronze/lavoura_semente_oxicoco.csv')
    semente_fada = lista[132][0]
    semente_fada.to_csv('docs_bronze/lavoura_semente_fada.csv')
    muda_uva = lista[136][0]
    muda_uva.to_csv('docs_bronze/lavoura_muda_uva.csv')
    # especial
    semente_rara = lista[140][0]
    semente_rara.to_csv('docs_bronze/lavoura_semente_rara.csv')
    semente_antiga = lista[142][0]
    semente_antiga.to_csv('docs_bronze/lavoura_semente_antiga.csv')
    semente_cacto = lista[144][0]
    semente_cacto.to_csv('docs_bronze/lavoura_semente_cacto.csv')
    semente_abacaxi = lista[147][0]
    semente_abacaxi.to_csv('docs_bronze/lavoura_semente_abacaxi.csv')
    broto_cha = lista[150][0]
    broto_cha.to_csv('docs_bronze/lavoura_broto_cha.csv')

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
    mangueira.to_csv('docs_bronze/arvores_manqueira.csv')
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
    maquina_maionese.to_csv('docs_bronze/mercadoria_paquina_maionese.csv')
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



if __name__ == '__main__':
    #import
    from bs4 import BeautifulSoup as bs4
    import pandas as pd
    from io import StringIO

    #execute
    #df_cultivo(html='docs_raw/sopa_Cultivo.html')
    #df_mineracao(html='docs_raw/sopa_Mineração.html')
    #df_coleta(html='docs_raw/sopa_Coleta.html')
    #df_pesca(html='docs_raw/sopa_Pesca.html')
    #df_combate(html='docs_raw/sopa_Combate.html')
    #df_lavouras(html='docs_raw/sopa_Lavouras.html')
    #df_animais(html='docs_raw/sopa_Animais.html')
    #df_arvores_frutiferas(html='docs_raw/sopa_Árvores_frutíferas.html')
    #df_mercadorias_artesanais(html='docs_raw/sopa_Mercadorias_Artesanais.html')
    #df_casa_fazenda(html='docs_raw/sopa_Casa_da_Fazenda.html')
    df_caverna(html='docs_raw/sopa_A_Caverna.html')