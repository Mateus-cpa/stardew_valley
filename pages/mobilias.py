import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  mobilias = pd.read_csv('docs_silver/mobilias.csv',encoding='utf-8')


  # Título
  st.title('Mobílias')
  st.metric('Tamanho da tabela', mobilias.shape[0])
  st.metric('Quantidade de colunas', mobilias.shape[1])

  st.dataframe(mobilias, use_container_width=True,hide_index=True)

  # fim da função

  

if __name__ == '__main__':
    main()
