import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  pescas_bau = pd.read_csv('docs_silver/pescas_bau.csv',encoding='utf-8')
  pescas_zona = pd.read_csv('docs_silver/pescas_zona.csv',encoding='utf-8')

  # Título
  st.title('Pescas de Baús')
  st.metric('Tamanho da tabela', pescas_bau.shape[0])
  st.metric('Quantidade de colunas', pescas_bau.shape[1])

  st.dataframe(pescas_bau, use_container_width=True,hide_index=True)

  st.title('Zonas de Pesca')
  st.metric('Tamanho da tabela', pescas_zona.shape[0])
  st.metric('Quantidade de colunas', pescas_zona.shape[1])

  st.dataframe(pescas_zona, use_container_width=True,hide_index=True)

  # fim da função

  

if __name__ == '__main__':
    main()
