import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  ferramentas = pd.read_csv('docs_silver/ferramentas.csv',encoding='utf-8').iloc[:,1:]


  # Título
  st.title('Ferramentas')
  
  
  # Cria colunas
  col1, col2, col3 = st.columns(3)
  
# Filtro
  filtro_texto = col1.text_input('Filtro por um termo')
  if filtro_texto:
     ferramentas = ferramentas[ferramentas.astype(str).apply(lambda x: x.str.contains(filtro_texto, case=False, na=False)).any(axis=1)].reset_index(drop=True)


  # select
  filtro_select = col3.multiselect('Filtro por Tipo', ferramentas['Tipo'].unique())
  if filtro_select:
    ferramentas = ferramentas[ferramentas['Tipo'].isin(filtro_select)].reset_index(drop=True)
    
  #KPIs
  col2.metric('Quantidade de resultados', ferramentas.shape[0])

  # dataframe
  if len(ferramentas) > 4:
     st.dataframe(ferramentas, hide_index=True)
  else:
     for i in ferramentas.index:
        st.subheader(f'{ferramentas.iloc[i,1]}')
        if not pd.isna(ferramentas.iloc[i,2]):
          st.write(f'Efeito: {ferramentas.iloc[i,2]}')
        if not pd.isna(ferramentas.iloc[i,3]):
          st.write(f'Preço (ouros): {ferramentas.iloc[i,3]}')
        if not pd.isna(ferramentas.iloc[i,4]):
          st.write(f'Materiais: {ferramentas.iloc[i,4]}')
        if not pd.isna(ferramentas.iloc[i,5]):
          st.write(f'Localização: {ferramentas.iloc[i,5]}')
        if not pd.isna(ferramentas.iloc[i,6]):
          st.write(f'Requisitos: {ferramentas.iloc[i,6]}')

  # fim da função

  

if __name__ == '__main__':
    main()