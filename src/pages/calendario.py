import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  calendario = pd.read_csv('docs_silver/calendario.csv',encoding='utf-8').iloc[:,1:]


  # Título
  st.title('Calendário')

  #filtro por evento
  filtro_evento = st.multiselect('Filtro por evento', calendario['Evento'].unique())
  filtro_mes = st.multiselect('Filtro por Mês', calendario['Mes'].unique())
  if filtro_evento:
    calendario = calendario[calendario['Evento'].isin(filtro_evento)]
  if filtro_mes:
    calendario = calendario[calendario['Mes'].isin(filtro_mes)]

  col1, col2, col3 = st.columns(3)
  col1.metric('Total de Eventos', calendario.shape[0])
  col2.metric('Aniversários', calendario[calendario['Evento'] == 'aniversario'].shape[0])
  col3.metric('Festivais', calendario[calendario['Evento'] == 'festivais'].shape[0])

  st.dataframe(calendario, hide_index=True)

  # fim da função

  

if __name__ == '__main__':
    main()