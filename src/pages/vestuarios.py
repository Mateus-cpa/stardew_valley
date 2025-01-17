import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  # Carregar os dados
  vestuarios = pd.read_csv('docs_silver/vestuarios.csv',encoding='utf-8')
  
  st.markdown('Vestuário')
  st.sidebar.markdown('Vestuário')
  st.title('Vestuário')
  st.dataframe(vestuarios)

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