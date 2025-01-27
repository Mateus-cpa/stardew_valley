import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  # menu
  pg = st.navigation([st.Page("animais.py"), 
                      st.Page("armas.py"), 
                      st.Page("artefatos.py"), 
                      st.Page("arvores.py"),
                      st.Page("atributos_luta.py")])
  pg.run()


    # fim da função


if __name__ == '__main__':
    main()
"""
streamlit run src/pages/dataviz.py


pg = st.navigation([st.Page("page_1.py"), st.Page("page_2.py")])
pg.run()
https://docs.streamlit.io/develop/concepts/multipage-apps/page-and-navigation
https://docs.streamlit.io/develop/quick-reference/cheat-sheet

"""
