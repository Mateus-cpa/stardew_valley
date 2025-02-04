import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  iscas = pd.read_csv('docs_silver/iscas.csv',encoding='utf-8')


  # Título
  st.title('Iscas')
  st.metric('Tamanho da tabela', iscas.shape[0])
  st.metric('Quantidade de colunas', iscas.shape[1])

  st.dataframe(iscas)

  # fim da função

  

if __name__ == '__main__':
    main()