import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  atributos_luta = pd.read_csv('docs_silver/atributos_luta.csv',encoding='utf-8')


  # Título
  st.title('Atributos de Luta')
  st.metric('Tamanho da tabela', atributos_luta.shape[0])
  st.metric('Quantidade de colunas', atributos_luta.shape[1])

  st.dataframe(atributos_luta)

  # fim da função

  

if __name__ == '__main__':
    main()