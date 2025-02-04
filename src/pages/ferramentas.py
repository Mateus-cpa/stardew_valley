import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  ferramentas = pd.read_csv('docs_silver/ferramentas.csv',encoding='utf-8')


  # Título
  st.title('Ferramentas')
  st.metric('Tamanho da tabela', ferramentas.shape[0])
  st.metric('Quantidade de colunas', ferramentas.shape[1])

  st.dataframe(ferramentas)

  # fim da função

  

if __name__ == '__main__':
    main()