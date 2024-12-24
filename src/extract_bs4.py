def extrair_sopa():
    # importações
    from bs4 import BeautifulSoup as bs
    import requests as rq
    import pandas as pd
    from io import StringIO


    paginas = ['Cultivo', #0
            'Mineração', #1
            'Coleta', #2
            'Pesca', #3
            'Combate', #4
            'Lavouras', #5
            'Animais', #6
            'Árvores_frutíferas', #7
            'Mercadorias_Artesanais', #8
            'Casa_da_Fazenda', #9
            'A_Caverna', #10
            'Estufa', #11
            'Casa', #12
            'Clima', #13
            'Primavera', #14
            'Verão', #15
            'Outono', #16
            'Inverno', #17
            'Festivais', #18
            'Monstros', #19
            'Televisão', #20
            'Aldeões', #21
            'Amizade', #22
            'Casamento', #23
            'Crianças', #24
            'Missões', #25
            'Conjuntos', #26
            'Conquistas', #27
            'Multijogador', #28
            'Modificações', #29
            'Ferramentas', #30
            'Armas', #31
            'Chapéus', #32
            'Calçados', #33
            'Anéis', #34
            'Peixes', #35
            'Isca', #36
            'Anzóis', #37
            'Fertilizante', #38
            'Culinária', #39
            'Artesanato', #40
            'Árvores', #41
            'Recados_Secretos', #42
            'Carteira', #43
            'Artefatos', #44
            'Minerais', #45
            'Mobília', #46
            'Papel_de_Parede', #47
            'Pisos', #48
            'Vila_Pelicanos', #49
            'Lista_de_Todos_os_Presentes', #50
            'Ferreiro', #51
            'Mercado_Joja', #52
            'Museu', #53,
            'Armazém_do_Pierre', #54
            'Saloon_Fruta_Estrelar', #55
            'Rancho_da_Marnie', #56
            'Casa_Arruinada', #57
            'Bosque_Secreto', #58
            'Torre_do_mago', #59
            'Peixaria', #60
            'A_Montanha', #61
            'Guilda_dos_Aventureiros', #62
            'Carpintaria', #63





            #outros
                ]

    for pagina in paginas:
        url = f'https://pt.stardewvalleywiki.com/{pagina}'
        sopa = bs(rq.get(url).text, 'html.parser')
        with open(f'docs/sopa_{pagina}.html', 'w', encoding='utf-8') as arquivo:
            arquivo.write(sopa.prettify())
    return sopa

if __name__ == '__main__':
    sopa = extrair_sopa()
    print(sopa[4])

