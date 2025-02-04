import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  animais = pd.read_csv('docs_silver/animais.csv',encoding='utf-8')


  # Título
  st.title('Animais')
  st.metric('Tamanho da tabela', animais.shape[0])
  st.metric('Quantidade de colunas', animais.shape[1])
  custo_animais = animais.Custo.mean()
  st.metric('Custo médio de animais', custo_animais)
  valor_produtos = round(animais.Produz_valor.mean())
  st.metric('Valor médio dos produtos', valor_produtos)
  st.metric('Rendimento médio de animal / produto', round(custo_animais/valor_produtos,2))
  
  st.dataframe(animais)
  
  
  # fim da função

  

if __name__ == '__main__':
    main()