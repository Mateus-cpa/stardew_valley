import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  casa = pd.read_csv('docs_silver/casa.csv',encoding='utf-8').iloc[:,1:]


  # Título
  st.title('Casa')
  filtro = st.text_input('Pesquise um termo para filtrar', '')
  if filtro:
    casa = casa[casa.astype(str).apply(lambda x: x.str.contains(filtro, case=False, na=False)).any(axis=1)].reset_index(drop=True)
  st.metric('Quantidade de resultados', casa.shape[0])

  
  if casa.shape[0] > 3:
    st.dataframe(casa, hide_index=True)

  for i in range(0,3): #mostrar se até 3 resultados e se tiver valor
    if casa.shape[0] == i+1:
      st.subheader(f'{casa['Nome'].values[i]}')
      st.write(f'**Tipo**: {casa['Tipo'].values[i]}')
      if not pd.isna(casa.loc[i,'Custo']):
        st.write(f'**Custo**: {casa.loc[i,'Custo']}')
      if not pd.isna(casa.loc[i,'Animais']):
        st.write(f'**Animais**: {casa.loc[i,'Animais']}')
      if not pd.isna(casa.loc[i,'Descrição']):
        st.write(f'**Descrição**: {casa.loc[i,'Descrição']}')
      if not pd.isna(casa.loc[i,'Tamanho']):
        st.write(f'**Tamanho**: {casa.loc[i,'Tamanho']}')
      if not pd.isna(casa.loc[i,'Detalhes']):
        st.write(f'**Detalhes**: {casa.loc[i,'Detalhes']}')
  # fim da função

  

if __name__ == '__main__':
    main()