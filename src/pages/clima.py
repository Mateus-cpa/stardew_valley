import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  clima = pd.read_csv('docs_silver/clima.csv',encoding='utf-8').iloc[:,1:]


  # Título
  st.title('Clima')
  
  filtro_texto = st.text_input('Filtrar resultados por um termo')
  if filtro_texto:
    clima = clima[clima.astype(str).apply(lambda x: x.str.contains(filtro_texto, case=False, na=False)).any(axis=1)].reset_index(drop=True)
  st.metric('Quantidade de resultados', clima.shape[0])

  if clima.shape[0] == 1:
    st.subheader(f'{clima["Clima"].values[0]}')
    st.text(f'Descrição: {clima["Descrição"].values[0]}')
  else:
    st.dataframe(clima, hide_index=True)

  # fim da função

  

if __name__ == '__main__':
    main()