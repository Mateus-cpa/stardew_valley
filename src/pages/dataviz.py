import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  # menu
  st.title('Página inicial')
  st.markdown('Navegue pelo menu à esquerda')
  
  
  st.sidebar.markdown('Árvores')
             
  st.markdown('Animais')
  st.sidebar.markdown('Animais')
  st.title('Animais')

  st.markdown('Armas')
  st.sidebar.markdown('Armas')
  st.title('Armas')
  
  st.markdown('Atributos de Luta')
  st.sidebar.markdown('Atributos de Luta')
  st.title('Atributos de Luta')
  
  st.markdown('Produtos')
  st.sidebar.markdown('Produtos')
  st.title('Produtos')
  
  st.markdown('Artefatos')
  st.sidebar.markdown('Artefatos')
  st.title('Artefatos')
  
  st.sidebar.markdown('Vestuário')
  st.title('Vestuário')
  
  st.markdown('Calendário')
  st.sidebar.markdown('Calendário')
  st.title('Calendário')
  
  st.markdown('Caverna')
  st.sidebar.markdown('Caverna')
  st.title('Caverna')
  
  st.markdown('Carteira')
  st.sidebar.markdown('Carteira')
  st.title('Carteira')
  
  st.markdown('Clima')
  st.sidebar.markdown('Clima')
  st.title('Clima')
  
  st.markdown('Coleta')
  st.sidebar.markdown('Coleta')
  st.title('Coleta')
  
  st.markdown('Conjunto')
  st.sidebar.markdown('Conjunto')
  st.title('Conjunto')
  
  st.markdown('Culinária')
  st.sidebar.markdown('Culinária')
  st.title('Culinária')
  
  st.markdown('Solo foliar')
  st.sidebar.markdown('Solo foliar')
  st.title('Solo foliar')
  
  st.markdown('Casa')
  st.sidebar.markdown('Casa')
  st.title('Casa')
  
  st.markdown('Ferramentas')
  st.sidebar.markdown('Ferramentas')
  st.title('Ferramentas')
  
  st.markdown('Iscas')
  st.sidebar.markdown('Iscas')
  st.title('Iscas')
  
  
  st.title('Árvores')
  
  
  """pg = st.navigation([st.Page("animais.py"), 
                      st.Page("armas.py"), 
                      st.Page("artefatos.py"), 
                      st.Page("arvores.py"),
                      st.Page("atributos_luta.py")])
  pg.run()"""


    # fim da função


if __name__ == '__main__':
    main()
"""
streamlit run src/pages/dataviz.py

your-repository/
├── page_1.py
├── page_2.py
└── streamlit_app.py


pg = st.navigation([st.Page("page_1.py"), st.Page("page_2.py")])
pg.run()
https://docs.streamlit.io/develop/concepts/multipage-apps/page-and-navigation
https://docs.streamlit.io/develop/quick-reference/cheat-sheet

"""
