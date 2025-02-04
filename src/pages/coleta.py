import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  coleta = pd.read_csv('docs_silver/coleta.csv',encoding='utf-8')


  # Título
  st.title('Coleta')
  st.metric('Tamanho da tabela', coleta.shape[0])
  st.metric('Quantidade de colunas', coleta.shape[1])

  st.dataframe(coleta)

  # fim da função

  

if __name__ == '__main__':
    main()