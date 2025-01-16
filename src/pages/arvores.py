import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  # Carregar os dados
  arvores = pd.read_csv('docs_silver/arvores.csv')
  

  st.markdown('Árvores')
  st.sidebar.markdown('Árvores')
  st.title('Árvores')
  st.dataframe(arvores)

  
  
  # fim da função

  


if __name__ == '__main__':
    main()
