import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  # Carregar os dados
  solo_foliar = pd.read_csv('docs_silver/solo_foliar.csv',encoding='utf-8')
  
  st.markdown('Solo foliar')
  st.sidebar.markdown('Solo foliar')
  st.title('Solo foliar')
  st.dataframe(solo_foliar)


if __name__ == '__main__':
    main()
