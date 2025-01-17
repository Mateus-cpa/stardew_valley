import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  # Carregar os dados
  caverna = pd.read_csv('docs_silver/caverna.csv',encoding='utf-8')
  
  st.markdown('Caverna')
  st.sidebar.markdown('Caverna')
  st.title('Caverna')
  st.dataframe(caverna)
  # fim da função

if __name__ == '__main__':
    main()
