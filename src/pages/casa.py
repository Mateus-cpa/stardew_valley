import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  casa = pd.read_csv('docs_silver/casa.csv',encoding='utf-8')


  # Título
  st.title('Casa')
  st.metric('Tamanho da tabela', casa.shape[0])
  st.metric('Quantidade de colunas', casa.shape[1])

  st.dataframe(casa)

  # fim da função

  

if __name__ == '__main__':
    main()