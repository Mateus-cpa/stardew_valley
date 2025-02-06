import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  pescas = pd.read_csv('docs_silver/pescas.csv',encoding='utf-8')


  # Título
  st.title('Pescas')
  st.metric('Tamanho da tabela', pescas.shape[0])
  st.metric('Quantidade de colunas', pescas.shape[1])

  st.dataframe(pescas, use_container_width=True,hide_index=True)

  # fim da função

  

if __name__ == '__main__':
    main()
