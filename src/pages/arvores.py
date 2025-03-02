import streamlit as st
import pandas as pd

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  arvores = pd.read_csv('docs_silver/arvores.csv',encoding='utf-8')


  # Título
  st.title('Árvores')
  
  #Filtro
  st.sidebar.title('Filtro')
  filtro = st.multiselect('Selecione a(s) árvore(s)', arvores['Muda'].unique())
  if filtro:
    arvores = arvores[arvores['Muda'].isin(filtro)]

  #KPIs
  col1, col2 = st.columns(2)
  with col1:
    st.metric('Quantidade de árvores', arvores['Muda'].nunique())
    st.metric('Média de Energia', round(arvores['Energia'].mean()))
    st.metric('Média de Saúde', round(arvores['Saude'].mean()))
    try:
      st.metric('Rentabilidade fruta/muda', round(arvores['Preco_venda'].mean() / arvores['preco_muda_pierre'].mean(), 4))
    except ValueError:
      st.metric('Rentabilidade fruta/muda', 0)
  with col2:
    st.metric('Média de Preço de venda da fruta', round(arvores['Preco_venda'].mean()))
    try:
      st.metric('Preço médio da muda no Pierre', round(arvores['preco_muda_pierre'].mean()))
      st.metric('Média de preço mínimo da muda no Carrinho de viagem', round(arvores['preco_minimo_muda_carrinho_viagem'].mean()))
      st.metric('Média de preço máximo da muda no Carrinho de viagem', round(arvores['preco_maximo_muda_carrinho_viagem'].mean()))
    except ValueError:
      st.metric('Preço médio da muda no Pierre', 0)
      st.metric('Média de preço mínimo da muda no Carrinho de viagem', 0)
      st.metric('Média de preço máximo da muda no Carrinho de viagem', 0)

  #Dataframe
  st.dataframe(arvores, hide_index=True)

  #Gráfico
  st.bar_chart(arvores,
               x='Fruta', y='Preco_venda',
               horizontal=True,)
  
  # fim da função

  

if __name__ == '__main__':
    main()