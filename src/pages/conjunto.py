import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  conjunto = pd.read_csv('docs_silver/conjuntos.csv',encoding='utf-8')


  # Título
  st.title('Conjunto')
  st.metric('Tamanho da tabela', conjunto.shape[0])
  st.metric('Quantidade de colunas', conjunto.shape[1])

  st.dataframe(conjunto)

  # fim da função

  

if __name__ == '__main__':
    main()