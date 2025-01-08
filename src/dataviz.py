import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados
profissoes = pd.read_csv('docs_silver/profissoes.csv')
animais = pd.read_csv('docs_silver/animais.csv')
armas = pd.read_csv('docs_silver/armas.csv')
artesanatos = pd.read_csv('docs_silver/artesanatos.csv')
atributos_luta = pd.read_csv('docs_silver/artesanatos.csv')
artefatos = pd.read_csv('docs_silver/artefatos.csv')

# Título da aplicação
st.title('Profissões')
st.dataframe(profissoes)

st.title('Animais')
st.dataframe(animais)

st.title('Armas')
st.dataframe(armas)

st.title('Atributos de Luta')
st.dataframe(atributos_luta)

st.title('Artesanato')
st.dataframe(artesanatos)

st.title('Artefatos')
st.dataframe(artefatos)

#streamlit run src/dataviz.py



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