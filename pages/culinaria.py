import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

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
  #fazer um filtro slider de preço de venda
  filtrar_por_venda = st.checkbox('Filtrar por preço de venda')
  if filtrar_por_venda:
    filtro_preco = st.slider('Filtre por preço de venda:', culinaria['Preço de Venda'].min(), culinaria['Preço de Venda'].max(), (culinaria['Preço de Venda'].min(), culinaria['Preço de Venda'].max()))  
    culinaria = culinaria[(culinaria['Preço de Venda'] >= filtro_preco[0]) & (culinaria['Preço de Venda'] <= filtro_preco[1])]
  # Retirar colunas que todos dados estão em branco
  culinaria = culinaria.dropna(axis=1, how='all')

  # KPIs
  col1, col2, col3, col4 = st.columns(4)
  col1.metric('Quantidade de resultados', culinaria.shape[0])
  if 'Preço de Venda' in culinaria.columns:
    col2.metric('Preço médio de venda', round(culinaria['Preço de Venda'].mean()))
  col3.metric('Saúde (média)', round(culinaria['Saúde'].mean()))
  col4.metric('Energia (média)', round(culinaria['Energia'].mean()))

  #dataframe
  st.dataframe(culinaria, hide_index=True)

  #gráfico
  
  st.write('Preço de venda')
  st.write(alt.Chart(culinaria).mark_point().encode(
    x='Saúde',
    y='Energia',
    color='Preço de Venda'
  ).properties(
    width=800,
    height=400
  ))

  # fim da função

  

if __name__ == '__main__':
    main()
