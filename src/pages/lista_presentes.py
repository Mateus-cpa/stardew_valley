import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  lista_presentes = pd.read_csv('docs_silver/lista_presentes.csv',encoding='utf-8')


  # Título
  st.title('Lsita de Presentes')
  st.metric('Tamanho da tabela', lista_presentes.shape[0])
  st.metric('Quantidade de colunas', lista_presentes.shape[1])

  st.dataframe(lista_presentes,
               hide_index=True,
               use_container_width=True,
               on_select='rerun',
               selection_mode='multi-row')

  # fim da função

  

if __name__ == '__main__':
    main()
