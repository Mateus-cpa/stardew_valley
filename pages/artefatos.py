import streamlit as st
import pandas as pd

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  artefatos = pd.read_csv('docs_silver/artefatos.csv',encoding='utf-8')
  artefatos = artefatos.iloc[:,1:5]


  # Título
  st.title('Artefatos')
  col1, col2, col3 = st.columns(3)

  with col1:
    st.metric('Tamanho da tabela', artefatos.shape[0])
  with col2:
    st.metric('Quantidade de colunas', artefatos.shape[1])
  with col3:
    st.metric('Valor médio de recompensa', round(artefatos.Preço.mean(),2))

  st.dataframe(artefatos, hide_index=True)

  # fim da função

  

if __name__ == '__main__':
    main()