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


  st.markdown('Profissões')
  st.sidebar.markdown('Profissões')
  st.title('Profissões')
  st.dataframe(profissoes)

  st.title('XP')
  def filter_dataframe(df, selected_values):
      if selected_values:
          filtered_df = df[df['Profissao'].isin(selected_values)]
      else:
          filtered_df = df
      return filtered_df

  selected_values = st.multiselect('Selecione filtro por Profissão:', xp['Profissao'].unique())# Create a multiselect widget for selecting values
  filtered_xp = filter_dataframe(xp, selected_values)# Filter the DataFrame based on selected values

  st.dataframe(filtered_xp)# Display the filtered DataFrame
  st.bar_chart(filtered_xp,x='item',
              y='XP',
              x_label='Item',
              y_label='Valor de Experiência',
              horizontal=True)

  st.markdown('Animais')
  st.sidebar.markdown('Animais')
  st.title('Animais')
  st.dataframe(animais)

  st.markdown('Armas')
  st.sidebar.markdown('Armas')
  st.title('Armas')
  st.dataframe(armas)

  st.markdown('Atributos de Luta')
  st.sidebar.markdown('Atributos de Luta')
  st.title('Atributos de Luta')
  st.dataframe(atributos_luta)

  st.markdown('Produtos')
  st.sidebar.markdown('Produtos')
  st.title('Produtos')
  st.dataframe(produtos)

  st.markdown('Artefatos')
  st.sidebar.markdown('Artefatos')
  st.title('Artefatos')
  st.dataframe(artefatos)

  st.markdown('Vestuário')
  st.sidebar.markdown('Vestuário')
  st.title('Vestuário')
  st.dataframe(vestuarios)

  st.markdown('Calendário')
  st.sidebar.markdown('Calendário')
  st.title('Calendário')
  st.dataframe(calendario)

  st.markdown('Caverna')
  st.sidebar.markdown('Caverna')
  st.title('Caverna')
  st.dataframe(caverna)

  st.markdown('Carteira')
  st.sidebar.markdown('Carteira')
  st.title('Carteira')
  st.dataframe(carteira)

  st.markdown('Clima')
  st.sidebar.markdown('Clima')
  st.title('Clima')
  st.dataframe(clima)

  st.markdown('Coleta')
  st.sidebar.markdown('Coleta')
  st.title('Coleta')
  st.dataframe(coleta)

  st.markdown('Conjunto')
  st.sidebar.markdown('Conjunto')
  st.title('Conjunto')
  st.dataframe(conjunto)

  st.markdown('Culinária')
  st.sidebar.markdown('Culinária')
  st.title('Culinária')
  st.dataframe(culinaria)

  st.markdown('Solo foliar')
  st.sidebar.markdown('Solo foliar')
  st.title('Solo foliar')
  st.dataframe(solo_foliar)

  st.markdown('Casa')
  st.sidebar.markdown('Casa')
  st.title('Casa')
  st.dataframe(casa)

  st.markdown('Ferramentas')
  st.sidebar.markdown('Ferramentas')
  st.title('Ferramentas')
  st.dataframe(ferramentas)

  st.markdown('Iscas')
  st.sidebar.markdown('Iscas')
  st.title('Iscas')
  st.dataframe(iscas)
  
  # fim da função

  

  st.title('Árvores')
  st.dataframe(arvores)

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