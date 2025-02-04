import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt

def main():
  # menu
  st.title('Página inicial')
  st.write('Navegue pelo menu abaixo para acessar as páginas disponíveis')

  if st.button('Animais'):
     st.switch_page("pages/animais.py")
  if st.button('Armas'):
     st.switch_page("pages/armas.py")
  if st.button('Artefatos'):
      st.switch_page("pages/artefatos.py")
  if st.button('Árvores'):
      st.switch_page("pages/arvores.py")
  if st.button('Atributos de Luta'):
      st.switch_page("pages/atributos_luta.py")
  if st.button('Calendário'):
      st.switch_page("pages/calendario.py")
  if st.button('Carteira'):
      st.switch_page("pages/carteira.py")
  if st.button('Casa'):
      st.switch_page("pages/casa.py")
  if st.button('Caverna'):
      st.switch_page("pages/caverna.py")
  if st.button('Clima'):
      st.switch_page("pages/clima.py")
  if st.button('Coleta'):
      st.switch_page("pages/coleta.py")
  if st.button('Conjunto'):
      st.switch_page("pages/conjunto.py")
  if st.button('Culinária'):
      st.switch_page("pages/culinaria.py")
  if st.button('Ferramentas'):
      st.switch_page("pages/ferramentas.py")
  if st.button('Iscas'):
      st.switch_page("pages/iscas.py")
  if st.button('Lavoura'):
     st.switch_page("pages/lavoura.py")
  if st.button('produtos'):
     st.switch_page("pages/produtos.py")
  if st.button('Profissões'):
     st.switch_page("pages/profissoes.py")
  if st.button('Solo foliar'):
     st.switch_page("pages/solo_foliar.py")
  if st.button('Vestuário'):
     st.switch_page("pages/vestuarios.py")
  if st.button('XP'):
     st.switch_page("pages/xp.py")

  st.image(os.path.join('src','pages','static','background-h.jpg'))

  
  
    # fim da função


if __name__ == '__main__':
    main()
"""
streamlit run src/pages/dataviz.py

https://docs.streamlit.io/develop/concepts/multipage-apps/page-and-navigation
https://docs.streamlit.io/develop/quick-reference/cheat-sheet

"""
