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
  st.metric('Tamanho da tabela', calendario.shape[0])
  st.metric('Quantidade de colunas', calendario.shape[1])

  st.dataframe(calendario)

  # fim da função

  

if __name__ == '__main__':
    main()