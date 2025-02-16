import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  animais = pd.read_csv('docs_silver/animais.csv',encoding='utf-8')
  animais = animais.drop(columns=['Unnamed: 0'])

  # Título
  st.title('Animais')
  st.metric('Tamanho da tabela', animais.shape[0])
  st.metric('Quantidade de colunas', animais.shape[1])
  custo_animais = animais.Custo.mean()
  st.metric('Custo médio de animais', custo_animais)
  valor_produtos = round(animais.Produz_valor.mean())
  st.metric('Valor médio dos produtos', valor_produtos)
  st.metric('Rendimento médio de produção', round(animais['Rendimento de produção'].mean(),2))
  st.metric('Rendimento por venda', round(animais['Rendimento de venda'].mean(),2))
  
  st.dataframe(animais, 
               hide_index=True, 
               on_select='rerun',
               selection_mode='multi-row')
  
  st.subheader('Gráfico de rendimento de produtos gerados')
  fig, ax = plt.subplots()
  #plotar rendimento de produção por nome
  animais = animais.sort_values(by='Rendimento de produção', ascending=False)
  animais.plot(kind='bar', ax=ax, x='Nome', y='Rendimento de produção')
  st.pyplot(fig)
  
  

  # fim da função

  

if __name__ == '__main__':
    main()