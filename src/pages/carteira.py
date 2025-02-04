import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  carteira = pd.read_csv('docs_silver/carteira.csv',encoding='utf-8')


  # Título
  st.title('Carteira')
  st.metric('Tamanho da tabela', carteira.shape[0])
  st.metric('Quantidade de colunas', carteira.shape[1])

  st.dataframe(carteira)

  # fim da função

  

if __name__ == '__main__':
    main()