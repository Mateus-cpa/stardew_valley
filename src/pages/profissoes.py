import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  # Carregar os dados
  profissoes = pd.read_csv('docs_silver/profissoes.csv')
  

  st.markdown('Profissões')
  st.sidebar.markdown('Profissões')
  st.title('Profissões')
  st.dataframe(profissoes)

   
  # fim da função

  
if __name__ == '__main__':
    main()
