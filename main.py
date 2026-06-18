# biblitecas nativas
import os

# bibliotecas instaladas
import streamlit as st

# importar bibliotecas locais

# pyrefly: ignore [missing-import]
from src.extract_bs4 import extrair_sopa as extrair

# pyrefly: ignore [missing-import]
from src.process_html_to_csv import processamento_geral

# pyrefly: ignore [missing-import]
from src.enrich_and_compile_csv import todas_funcoes_enriquecimento


def init_streamlit():

    st.title("Stardew Valley")
    st.write("Bem-vindo ao Stardew Valley")
    if st.sidebar.button("iniciar scraping"):
        extrair()  # importa html
        # botão de limpar tela
        if st.sidebar.button("limpar tela"):
            st.clear()
    if st.sidebar.button("processar html"):
        processamento_geral()  # raw (html) => bronze (csv)
        todas_funcoes_enriquecimento()  # bronze (csv) => silver (csv)

    col1, col2, col3, col4, col5 = st.columns(5)
    # listar arquivos na pasta pages
    lista_paginas = os.listdir("pages")

    for i, pagina in enumerate(lista_paginas):
        nome_pagina = pagina.split(".")[0].replace("_", " ")
        # dividir em 5 colunas
        if i % 5 == 0:
            if col1.button(nome_pagina):
                st.switch_page(f"pages/{pagina}")
        if i % 5 == 1:
            if col2.button(nome_pagina):
                st.switch_page(f"pages/{pagina}")
        if i % 5 == 2:
            if col3.button(nome_pagina):
                st.switch_page(f"pages/{pagina}")
        if i % 5 == 3:
            if col4.button(nome_pagina):
                st.switch_page(f"pages/{pagina}")
        if i % 5 == 4:
            if col5.button(nome_pagina):
                st.switch_page(f"pages/{pagina}")


if __name__ == "__main__":
    init_streamlit()
