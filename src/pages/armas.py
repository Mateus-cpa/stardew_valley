import streamlit as st
import pandas as pd

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  armas = pd.read_csv('docs_silver/armas.csv',encoding='utf-8')


  # Título
  st.title('Armas')
  st.metric('Tamanho da tabela', armas.shape[0])
  st.metric('Quantidade de colunas', armas.shape[1])

  st.dataframe(armas)

  # fim da função

  

if __name__ == '__main__':
    main()