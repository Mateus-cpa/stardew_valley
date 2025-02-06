import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  nos_minerios = pd.read_csv('docs_silver/nos_minerios.csv',encoding='utf-8')


  # Título
  st.title('Nós de Minerios')
  st.metric('Tamanho da tabela', nos_minerios.shape[0])
  st.metric('Quantidade de colunas', nos_minerios.shape[1])

  st.dataframe(nos_minerios, use_container_width=True,hide_index=True)

  # fim da função

  

if __name__ == '__main__':
    main()
