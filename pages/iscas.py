import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  iscas = pd.read_csv('docs_silver/iscas.csv',encoding='utf-8').iloc[:,1:]


  # Título
  st.title('Iscas')
  
  col1, col2 = st.columns(2)
  
  # Filtro
  filtro_texto = col1.text_input('Filtro por um termo')
  if filtro_texto:
     iscas = iscas[iscas.astype(str).apply(lambda x: x.str.contains(filtro_texto, case=False, na=False)).any(axis=1)].reset_index(drop=True)
  #KPIs 
  col2.metric('Quantidade de resultados', iscas.shape[0])
  
  # dataframe
  if len(iscas) > 2:
     st.dataframe(iscas, hide_index=True)
  else:
     for i in iscas.index:
      st.subheader(f'{iscas.iloc[i,0]}')
      if not pd.isna(iscas.iloc[i,1]):
        st.write(f'**Descrição**: {iscas.iloc[i,1]}')
      if not pd.isna(iscas.iloc[i,2]):
        st.write(f'**Notas**: {iscas.iloc[i,2]}')
      if not pd.isna(iscas.iloc[i,3]):
        st.write(f'**Custo (ouros)**: {iscas.iloc[i,3]}')
      if not pd.isna(iscas.iloc[i,4]):
        st.write(f'**Custo (produtos)**: {iscas.iloc[i,4]}')


  # fim da função

  

if __name__ == '__main__':
    main()