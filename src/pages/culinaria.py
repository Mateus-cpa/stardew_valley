import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  # Carregar os dados
  culinaria = pd.read_csv('docs_silver/culinaria.csv',encoding='utf-8')
  
  st.markdown('Culinária')
  st.sidebar.markdown('Culinária')
  st.title('Culinária')
  st.dataframe(culinaria)


if __name__ == '__main__':
    main()
