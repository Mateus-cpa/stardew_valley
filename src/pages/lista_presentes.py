import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  lista_presentes = pd.read_csv('docs_silver/lista_presentes.csv',encoding='utf-8').iloc[:,1:]


  # Título
  st.title('Lsita de Presentes')

  #filtros
  col1, col2 = st.columns(2)
  filtro_texto = col2.text_input('Filtre por um termo')
  if filtro_texto:
     lista_presentes = lista_presentes[
        lista_presentes.apply(lambda row: row.astype(str).str.contains(filtro_texto, case=False).any(), axis=1)
    ]
  col1.metric('Qtde de resultados', lista_presentes.shape[0])

  st.dataframe(lista_presentes,
               hide_index=True,
               use_container_width=True,
               on_select='rerun',
               selection_mode='multi-row')

  # fim da função

  

if __name__ == '__main__':
    main()
