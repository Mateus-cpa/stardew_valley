import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  # Carregar os dados
  profissoes = pd.read_csv('docs_silver/profissoes.csv')
  animais = pd.read_csv('docs_silver/animais.csv')
  armas = pd.read_csv('docs_silver/armas.csv')
  produtos = pd.read_csv('docs_silver/produtos.csv')
  atributos_luta = pd.read_csv('docs_silver/atributos_luta.csv')
  artefatos = pd.read_csv('docs_silver/artefatos.csv')
  xp = pd.read_csv('docs_silver/xp.csv',encoding='utf-8')
  arvores = pd.read_csv('docs_silver/arvores.csv',encoding='utf-8')
  vestuarios = pd.read_csv('docs_silver/vestuarios.csv',encoding='utf-8')
  calendario = pd.read_csv('docs_silver/calendario.csv',encoding='utf-8')
  carteira = pd.read_csv('docs_silver/carteira.csv',encoding='utf-8')
  caverna = pd.read_csv('docs_silver/caverna.csv',encoding='utf-8')
  clima = pd.read_csv('docs_silver/clima.csv',encoding='utf-8')
  coleta = pd.read_csv('docs_silver/coleta.csv',encoding='utf-8')
  conjunto = pd.read_csv('docs_silver/conjuntos.csv',encoding='utf-8')
  culinaria = pd.read_csv('docs_silver/culinaria.csv',encoding='utf-8')
  solo_foliar = pd.read_csv('docs_silver/solo_foliar.csv',encoding='utf-8')
  casa = pd.read_csv('docs_silver/casa.csv',encoding='utf-8')
  ferramentas = pd.read_csv('docs_silver/ferramentas.csv',encoding='utf-8')
  iscas = pd.read_csv('docs_silver/iscas.csv',encoding='utf-8')
  lavoura = pd.read_csv('docs_silver/lavouras.csv',encoding='utf-8')


  # Título
  st.markdown('Lavoura')
  st.sidebar.markdown('Lavoura')
  st.title('Lavoura')
  st.dataframe(lavoura)

  
  # fim da função

  

if __name__ == '__main__':
    main()
"""
streamlit run src/dataviz.py



your-repository/
├── page_1.py
├── page_2.py
└── streamlit_app.py

pg = st.navigation([st.Page("page_1.py"), st.Page("page_2.py")])
pg.run()
https://docs.streamlit.io/develop/concepts/multipage-apps/page-and-navigation
https://docs.streamlit.io/develop/quick-reference/cheat-sheet

"""


"""def grafico_xp ():
  #xp cultivo
  sns.boxplot(data=df_xp_cultivos, y='Estacao', x='XP', hue='Estacao')

  df_xp_cultivos = df_xp_cultivos.sort_values(by='XP', ascending=False)
  with sns.axes_style('whitegrid'):
    grafico = sns.barplot(data=df_xp_cultivos, y='Cultivo', x='XP', hue='Estacao', width = 0.8)
    grafico.set_title('XP por cultivo')
    grafico.set_xlabel('XP')
    grafico.set_ylabel('Cultivo')
    #tamanho do gráfico
    grafico.figure.set_size_inches(10, 20)
    
  #qualidade cultivo
  #fixar cores da legenda
  
  pass

"""