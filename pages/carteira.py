import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  carteira = pd.read_csv('docs_silver/carteira.csv',encoding='utf-8').iloc[:,1:]


  # Título
  st.title('Carteira')

  #filtro de pesquisa em todos os campos
  filtro = st.text_input('Pesquise um termo', '')
  if filtro:
    carteira = carteira[carteira.astype(str).apply(lambda x: x.str.contains(filtro, case=False, na=False)).any(axis=1)].reset_index(drop=True)
  st.metric('Qtde. de resultados', carteira.shape[0])

  if carteira.shape[0] > 3:
    st.dataframe(carteira, hide_index=True)

  for i in range(0,3): #mostrar se até 3 resultados e se tiver valor
    if carteira.shape[0] == i+1:
      st.subheader(f'{carteira['Nome'].values[i]}')
      if not pd.isna(carteira.loc[i,'Uso']):
        st.write(f'**Uso**: {carteira.loc[i,'Uso']}')
      if not pd.isna(carteira.loc[i,'Obtenção']):
        st.write(f'**Obtenção**: {carteira.loc[i,'Obtenção']}')
      if not pd.isna(carteira.loc[i,'Descrição']):
        st.write(f'**Descrição**: {carteira.loc[i,'Descrição']}')
      if not pd.isna(carteira.loc[i,'Localização']):
        st.write(f'**Localização**: {carteira.loc[i,'Localização']}')

  # fim da função

  

if __name__ == '__main__':
    main()