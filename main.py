def init_streamlit():
    # importação
    import streamlit as st

    # importar bibliotecas locais
    from src.extract_bs4 import extrair_sopa as extrair
    from src.process_html_to_csv import processamento_geral

    st.title("Stardew Valley")
    st.write("Bem-vindo ao Stardew Valley")
    if st.button("iniciar scraping"):
        extrair()  # importa html
        # botão de limpar tela
        if st.button("limpar tela"):
            st.clear()
    if st.button("processar html"):
        processamento_geral()  # html => csv


if __name__ == "__main__":
    init_streamlit()
