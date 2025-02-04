import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  solo_foliar = pd.read_csv('docs_silver/solo_foliar.csv',encoding='utf-8')


  # Título
  st.title('Solo Foliar')
  st.metric('Tamanho da tabela', solo_foliar.shape[0])
  st.metric('Quantidade de colunas', solo_foliar.shape[1])

  st.dataframe(solo_foliar)

  # fim da função

  

if __name__ == '__main__':
    main()