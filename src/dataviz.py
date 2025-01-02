import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados
profissoes = pd.read_csv('docs_silver/profissoes.csv')
animais = pd.read_csv('docs_silver/animais.csv')
armas = pd.read_csv('docs_silver/armas.csv')
artesanatos = pd.read_csv('docs_silver/artesanatos.csv')

# Título da aplicação
st.title('Profissões')
st.dataframe(profissoes)

st.title('Animais')
st.dataframe(animais)

st.title('Armas')
st.dataframe(armas)

st.title('Artesanato')
st.dataframe(artesanatos)


#streamlit run src/dataviz.py