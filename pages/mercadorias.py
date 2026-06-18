import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  mercadorias = pd.read_csv('docs_silver/mercadorias.csv',encoding='utf-8')


  # Título
  st.title('Mercadorias')
  st.metric('Tamanho da tabela', mercadorias.shape[0])
  st.metric('Quantidade de colunas', mercadorias.shape[1])

  st.dataframe(mercadorias, use_container_width=True,hide_index=True)

  # fim da função

  

if __name__ == '__main__':
    main()
