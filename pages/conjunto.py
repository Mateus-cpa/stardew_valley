import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  conjunto = pd.read_csv('docs_silver/conjuntos.csv',encoding='utf-8').iloc[:,1:]

  # Título
  st.title('Conjuntos')

  #filtro
  filtro_texto = st.text_input('Filtrar resultados por um termo')
  if filtro_texto:
    conjunto = conjunto[conjunto.astype(str).apply(lambda x: x.str.contains(filtro_texto, case=False, na=False)).any(axis=1)].reset_index(drop=True)

  #Kpis
  col1, col2, col3 = st.columns(3)
  col2.metric('Quantidade de resultados', conjunto.shape[0])
  
  #dataframe
  if conjunto['Conjunto'].nunique() > 1:
    st.dataframe(conjunto, hide_index=True)
  else:
    st.subheader(f'{conjunto.iloc[0,0]}')
    st.dataframe(conjunto.iloc[:,1:3], hide_index=True)
    st.write(f'**Recompensa**: {conjunto.iloc[0,3]}')


  # fim da função

  

if __name__ == '__main__':
    main()