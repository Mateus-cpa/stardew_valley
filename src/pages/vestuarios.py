import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  vestuario = pd.read_csv('docs_silver/vestuarios.csv',encoding='utf-8')


  # Título
  st.title('Vestuário')
  st.metric('Tamanho da tabela', vestuario.shape[0])
  st.metric('Quantidade de colunas', vestuario.shape[1])

  st.dataframe(vestuario)

  # fim da função

  

if __name__ == '__main__':
    main()