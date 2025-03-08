import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  culinaria = pd.read_csv('docs_silver/culinaria.csv',encoding='utf-8').iloc[:,1:]


  # Título
  st.title('Culinária')

  #Filtro
  filtro = st.multiselect('Filtre por tipos de ingredientes', culinaria.Tipo.unique())
  if filtro:
    culinaria = culinaria[culinaria.Tipo.isin(filtro)]
  # Retirar colunas que todos dados estão em branco
  culinaria = culinaria.dropna(axis=1, how='all')
  st.dataframe(culinaria, hide_index=True)

  # KPIs
  col1, col2, col3 = st.columns(3)
  col1.metric('Quantidade de resultados', culinaria.shape[0])
  col2.metric('Quantidade de colunas', culinaria.shape[1])
  if 'Preço de Venda' in culinaria.columns:
    st.metric('Preço médio de venda', culinaria['Preço de Venda'].mean())


  st.dataframe(culinaria, hide_index=True)

  # fim da função

  

if __name__ == '__main__':
    main()
