import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  culinaria = pd.read_csv('docs_silver/culinaria.csv',encoding='utf-8')


  # Título
  st.title('Culinária')
  st.metric('Tamanho da tabela', culinaria.shape[0])
  st.metric('Quantidade de colunas', culinaria.shape[1])

  st.dataframe(culinaria)

  # fim da função

  

if __name__ == '__main__':
    main()
