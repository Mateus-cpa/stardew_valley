import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  caverna = pd.read_csv('docs_silver/caverna.csv',encoding='utf-8')
  
  st.title('Caverna')
  st.dataframe(caverna)
  # fim da função

if __name__ == '__main__':
    main()
