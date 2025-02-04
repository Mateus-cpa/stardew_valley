import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  clima = pd.read_csv('docs_silver/clima.csv',encoding='utf-8')


  # Título
  st.title('Clima')
  st.metric('Tamanho da tabela', clima.shape[0])
  st.metric('Quantidade de colunas', clima.shape[1])

  st.dataframe(clima)

  # fim da função

  

if __name__ == '__main__':
    main()