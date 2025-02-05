import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  lavoura = pd.read_csv('docs_silver/lavouras.csv',encoding='utf-8')


  # Título
  st.title('Lavoura')
  st.metric('Tamanho da tabela', lavoura.shape[0])
  st.metric('Quantidade de colunas', lavoura.shape[1])

  st.dataframe(lavoura, use_container_width=True,hide_index=True)

  # fim da função

  

if __name__ == '__main__':
    main()
