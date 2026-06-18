import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  profissoes = pd.read_csv('docs_silver/profissoes.csv',encoding='utf-8')


  # Título
  st.title('Profissões')
  st.metric('Tamanho da tabela', profissoes.shape[0])
  st.metric('Quantidade de colunas', profissoes.shape[1])

  st.dataframe(profissoes)

  # fim da função

  

if __name__ == '__main__':
    main()
