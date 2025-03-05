import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  caverna = pd.read_csv('docs_silver/caverna.csv',encoding='utf-8').iloc[:,1:]
  
  st.title('Caverna')

  #filtro
  filtro_texto = st.text_input('Filtrar resultados por um termo')
  if filtro_texto:
    caverna = caverna[caverna.astype(str).apply(lambda x: x.str.contains(filtro_texto, case=False, na=False)).any(axis=1)].reset_index(drop=True)
  filtro_numerico = st.multiselect('Filtrar resultados por valor de', caverna.columns[2:5], key='filtro_numerico')
  if filtro_numerico:
    for col in filtro_numerico:
      minimo, maximo = st.slider(f'Filtrar por {col}', float(caverna[col].min()), float(caverna[col].max()), (float(caverna[col].min()), float(caverna[col].max())))
      caverna = caverna[(caverna[col] >= minimo) & (caverna[col] <= maximo)].reset_index(drop=True)
  
  #KPIs
  col1, col2, col3, col4, col5 = st.columns(5)
  with col1:
    st.metric('Resultados', caverna.shape[0])
  with col2:
     st.metric('Lucro (médio)', round(caverna['Lucro'].mean(),1))
  with col3:
    st.metric('Energia (média)', round(caverna['Energia'].mean(),1))
  with col4:
    st.metric('Saúde (média)', round(caverna['Saude'].mean(),1))
  with col5:
    st.metric('Chance (média)', round(caverna['Chance_%'].mean(),1))
  
  if caverna.shape[0] > 12:
    st.dataframe(caverna, hide_index=True)
  else:
    st.dataframe(caverna.iloc[:,0:6],hide_index=True, width=1000, height=caverna.shape[0]*44)
    #retirar coluna nome e pegar 1 linha de cada nome_original
    caverna_filtrada = caverna.drop(columns=['Nome']).drop_duplicates(subset='nome_original').reset_index(drop=True)
    for i in range(0,caverna_filtrada.shape[0]): #mostrar se != None
      st.subheader(f'{caverna_filtrada['nome_original'].values[i]}')
      if not pd.isna(caverna_filtrada.loc[i,'Usado em']):
        st.write(f'**Usado em**: {caverna_filtrada.loc[i,'Usado em']}')
      if not pd.isna(caverna_filtrada.loc[i,'Chance_%']):
        st.write(f'**Chance (%)**: {caverna_filtrada.loc[i,'Chance_%']}')
      if not pd.isna(caverna_filtrada.loc[i,'Descrição']):
        st.write(f'**Descrição**: {caverna_filtrada.loc[i,'Descrição']}')
      if not pd.isna(caverna_filtrada.loc[i,'Também achado']):
        st.write(f'**Também achado em**: {caverna_filtrada.loc[i,'Também achado']}')

  #gráfico
  st.scatter_chart(caverna, x='Saude', y='Energia', color='nome_original', width=0, height=0, use_container_width=True)

  #fim da função
if __name__ == '__main__':
    main()
