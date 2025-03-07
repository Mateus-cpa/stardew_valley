import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  coleta = pd.read_csv('docs_silver/coleta.csv',encoding='utf-8')


  # Título
  st.title('Coleta')
  
  #filtro
  filtro_texto = st.text_input('Filtrar resultados por um termo')
  if filtro_texto:
    coleta = coleta[coleta.astype(str).apply(lambda x: x.str.contains(filtro_texto, case=False, na=False)).any(axis=1)].reset_index(drop=True)
  filtro_numerico = st.multiselect('Filtrar resultados por valor de', coleta.columns[2:5], key='filtro_numerico')
  if filtro_numerico:
    for col in filtro_numerico:
      minimo, maximo = st.slider(f'Filtrar por {col}', float(coleta[col].min()), float(coleta[col].max()), (float(coleta[col].min()), float(coleta[col].max())))
      coleta = coleta[(coleta[col] >= minimo) & (coleta[col] <= maximo)].reset_index(drop=True)
  
  #KPIs
  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric('Resultados', coleta.shape[0])
  with col2:
     st.metric('Lucro (médio)', round(coleta['Lucro'].mean(),1))
  with col3:
    st.metric('Energia (média)', round(coleta['Energia'].mean(),1))
  with col4:
    st.metric('Saúde (média)', round(coleta['Saude'].mean(),1))
 
  
  if coleta.shape[0] > 12:
    st.dataframe(coleta, hide_index=True)
  else:
    st.dataframe(coleta.iloc[:,0:6],hide_index=True, width=1000, height=coleta.shape[0]*44)
    #retirar coluna nome e pegar 1 linha de cada nome_original
    coleta['nome_original'] = coleta['Nome'].str.split('_',expand=True)[0].str.strip()
    coleta_filtrada = coleta.drop(columns=['Nome']).drop_duplicates(subset='nome_original').reset_index(drop=True)
    for i in range(0,coleta_filtrada.shape[0]): #mostrar se != None
      st.subheader(f'{coleta_filtrada['nome_original'].values[i]}')
      if not pd.isna(coleta_filtrada.loc[i,'origem']):
        st.write(f'**Usado em**: {coleta_filtrada.loc[i,'origem']}')
      if not pd.isna(coleta_filtrada.loc[i,'Usado em']):
        st.write(f'**Usado em**: {coleta_filtrada.loc[i,'Usado em']}')
      if not pd.isna(coleta_filtrada.loc[i,'Encontrado em']):
        st.write(f'**Encontrado em**: {coleta_filtrada.loc[i,'Encontrado em']}')
      if not pd.isna(coleta_filtrada.loc[i,'Descrição']):
        st.write(f'**Descrição**: {coleta_filtrada.loc[i,'Descrição']}')

  #gráfico
  st.scatter_chart(coleta, x='Saude', y='Energia', color='origem', width=0, height=0, use_container_width=True)

  # fim da função

  

if __name__ == '__main__':
    main()