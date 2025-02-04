import streamlit as st
import pandas as pd

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  artefatos = pd.read_csv('docs_silver/artefatos.csv',encoding='utf-8')


  # Título
  st.title('Artefatos')
  st.metric('Tamanho da tabela', artefatos.shape[0])
  st.metric('Quantidade de colunas', artefatos.shape[1])

  st.dataframe(artefatos)

  # fim da função

  

if __name__ == '__main__':
    main()