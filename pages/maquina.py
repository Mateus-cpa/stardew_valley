import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  maquinas = pd.read_csv('docs_silver/maquinas.csv',encoding='utf-8')


  # Título
  st.title('Máquinas')
  st.metric('Tamanho da tabela', maquinas.shape[0])
  st.metric('Quantidade de colunas', maquinas.shape[1])

  st.dataframe(maquinas, use_container_width=True,hide_index=True)

  # fim da função

  

if __name__ == '__main__':
    main()
