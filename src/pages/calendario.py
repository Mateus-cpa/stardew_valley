import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  calendario = pd.read_csv('docs_silver/calendario.csv',encoding='utf-8')


  # Título
  st.title('Calendário')
  col1, col2 = st.columns(2)
  col1.metric('Tamanho da tabela', calendario.shape[0])
  col2.metric('Quantidade de colunas', calendario.shape[1])

  st.dataframe(calendario)

  # fim da função

  

if __name__ == '__main__':
    main()