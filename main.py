def pipeline():
    #importações
    import pandas as pd
    from io import StringIO
    from bs4 import BeautifulSoup as bs4

    #bibliotecas locais
    from src.extract_bs4 import extrair_sopa as extrair
    from src.process_html_to_csv import df_cultivo

    extrair()
    df_cultivo(html='docs\sopa_Cultivo.html')


if __name__ == '__main__':
    pipeline()
    