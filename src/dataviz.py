import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados
profissoes = pd.read_csv('docs_silver/profissoes.csv')

# Título da aplicação
st.title('Profissões')

st.dataframe(profissoes)
