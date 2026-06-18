import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  minerais = pd.read_csv('docs_silver/minerais.csv',encoding='utf-8')


  # Título
  st.title('Minerais')
  st.metric('Tamanho da tabela', minerais.shape[0])
  st.metric('Quantidade de colunas', minerais.shape[1])

  st.dataframe(minerais, use_container_width=True,hide_index=True)

  # fim da função

  

if __name__ == '__main__':
    main()
