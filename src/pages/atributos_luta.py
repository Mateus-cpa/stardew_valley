import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  atributos_luta = pd.read_csv('docs_silver/atributos_luta.csv',encoding='utf-8').iloc[:,1:]


  # Título
  st.title('Atributos de Luta')
  col1, col2 = st.columns(2)
  col1.metric('Tamanho da tabela', atributos_luta.shape[0])
  col2.metric('Quantidade de colunas', atributos_luta.shape[1])
 
  st.dataframe(atributos_luta,hide_index=True)

  # fim da função

  

if __name__ == '__main__':
    main()