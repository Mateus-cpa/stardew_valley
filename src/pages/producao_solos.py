import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  producao_solos = pd.read_csv('docs_silver/solos_producao.csv',encoding='utf-8')


  # Título
  st.title('Produção de Solos')
  st.metric('Tamanho da tabela', producao_solos.shape[0])
  st.metric('Quantidade de colunas', producao_solos.shape[1])

  st.dataframe(producao_solos, use_container_width=True,hide_index=True)

  # fim da função

  

if __name__ == '__main__':
    main()
