import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados
profissoes = pd.read_csv('docs_silver/profissoes.csv')
animais = pd.read_csv('docs_silver/animais.csv')
armas = pd.read_csv('docs_silver/armas.csv')
produtos = pd.read_csv('docs_silver/produtos.csv')
atributos_luta = pd.read_csv('docs_silver/atributos_luta.csv')
artefatos = pd.read_csv('docs_silver/artefatos.csv')
xp = pd.read_csv('docs_silver/xp.csv',encoding='utf-8')
arvores = pd.read_csv('docs_silver/arvores.csv',encoding='utf-8')


# Título da aplicação
st.title('Profissões')
st.dataframe(profissoes)

st.title('Animais')
st.dataframe(animais)

st.title('Armas')
st.dataframe(armas)

st.title('Atributos de Luta')
st.dataframe(atributos_luta)

st.title('Produtos')
st.dataframe(produtos)

st.title('Artefatos')
st.dataframe(artefatos)

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

st.title('Árvores')
st.dataframe(arvores)

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
