def df_cultivo(html):
     
    with open(html, 'r', encoding= 'utf-8') as f:
        html_cultivo = f.read()
    
    sopa = bs4(html_cultivo, 'html.parser')


    lista = []
    for tabela in sopa.find_all('table'):
        lista.append(pd.read_html(StringIO(str(tabela))))
        
    for i in range(len(lista)):
        for j in range(len(lista[i])):
            print(f'i = {i}, j = {j}')
            #print(lista[i][j])
        print('*-* FIM DA TABELA *-*'*5)

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


    profissao_cultivo.to_csv("docs_silver/profissao_cultivo.csv")

    pass


if __name__ == '__main__':
    #import
    from bs4 import BeautifulSoup as bs4
    import pandas as pd
    from io import StringIO
    df_cultivo = df_cultivo(html='docs/sopa_Cultivo.html')
    print(df_cultivo)