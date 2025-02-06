import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  peixes = pd.read_csv('docs_silver/peixes.csv',encoding='utf-8')


  # Título
  st.title('Peixes')
  st.metric('Tamanho da tabela', peixes.shape[0])
  st.metric('Quantidade de colunas', peixes.shape[1])

  st.dataframe(peixes, use_container_width=True,hide_index=True)

  # fim da função

  

if __name__ == '__main__':
    main()
