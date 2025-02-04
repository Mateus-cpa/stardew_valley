import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  produtos = pd.read_csv('docs_silver/produtos.csv',encoding='utf-8')


  # Título
  st.title('Produtos')
  st.metric('Tamanho da tabela', produtos.shape[0])
  st.metric('Quantidade de colunas', produtos.shape[1])

  st.dataframe(produtos)

  # fim da função

  

if __name__ == '__main__':
    main()