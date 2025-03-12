import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  ferramentas = pd.read_csv('docs_silver/ferramentas.csv',encoding='utf-8')


  # Título
  st.title('Ferramentas')
  
  # Filtro
  filtro_texto = st.text_input('Filtro por um termo')
  if filtro_texto:
     ferramentas = ferramentas[ferramentas.astype(str).apply(lambda x: x.str.contains(filtro_texto, case=False, na=False)).any(axis=1)].reset_index(drop=True)

  col1, col2, col3 = st.columns(3)

  col2.metric('Quantidade de resultados', ferramentas.shape[0])

  
  st.dataframe(ferramentas)

  # fim da função

  

if __name__ == '__main__':
    main()