import streamlit as st
import pandas as pd

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  arvores = pd.read_csv('docs_silver/arvores.csv',encoding='utf-8')


  # Título
  st.title('Árvores')
  st.metric('Tamanho da tabela', arvores.shape[0])
  st.metric('Quantidade de colunas', arvores.shape[1])

  st.dataframe(arvores)

  # fim da função

  

if __name__ == '__main__':
    main()