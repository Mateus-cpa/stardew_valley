import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  missoes = pd.read_csv('docs_silver/missoes.csv',encoding='utf-8')


  # Título
  st.title('Missões')
  st.metric('Tamanho da tabela', missoes.shape[0])
  st.metric('Quantidade de colunas', missoes.shape[1])

  st.dataframe(missoes, use_container_width=True,hide_index=True)

  # fim da função

  

if __name__ == '__main__':
    main()
