import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  taxa_cultivo = pd.read_csv('docs_silver/taxas_cultivo.csv',encoding='utf-8')


  # Título
  st.title('Taxas de cultivo')
  st.metric('Tamanho da tabela', taxa_cultivo.shape[0])
  st.metric('Quantidade de colunas', taxa_cultivo.shape[1])

  st.dataframe(taxa_cultivo, use_container_width=True,hide_index=True)

  # fim da função

  

if __name__ == '__main__':
    main()
