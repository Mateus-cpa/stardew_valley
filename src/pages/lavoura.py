import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  # Carregar os dados
  lavoura = pd.read_csv('docs_silver/lavouras.csv',encoding='utf-8')


  # Título
  st.title('Lavoura')
  st.metric('Tamanho da tabela', lavoura.shape[0])
  st.metric('Quantidade de colunas', lavoura.shape[1])

  st.dataframe(lavoura)

  
  # fim da função

  

if __name__ == '__main__':
    main()
"""
streamlit run src/pages/lavoura.py

pg = st.navigation([st.Page("page_1.py"), st.Page("page_2.py")])
pg.run()
https://docs.streamlit.io/develop/concepts/multipage-apps/page-and-navigation
https://docs.streamlit.io/develop/quick-reference/cheat-sheet

"""
