import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt

def main():
  # menu
    st.title('Página inicial')
    st.write('Navegue pelo menu abaixo para acessar as páginas disponíveis')

#criar container e alinhas os botões em 3 colunas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
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
        
    with col2:
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
        
    with col3:
        
        if st.button('Lista de presentes'):
            st.switch_page("pages/lista_presentes.py")
        if st.button('Máquina'):
            st.switch_page("pages/maquina.py")
        if st.button('Mercadorias'):
            st.switch_page("pages/mercadorias.py")
        if st.button('Minerais'):
            st.switch_page("pages/minerais.py")
        if st.button('Missões'):
            st.switch_page("pages/missoes.py")
        if st.button('Mobílias'):
            st.switch_page("pages/mobilias.py")
        if st.button('Nós de Minério'):
            st.switch_page("pages/nos_minerio.py")
        if st.button('Peixes'):
            st.switch_page("pages/peixes.py")
        
    with col4:
        
        if st.button('Pescas'):
            st.switch_page("pages/pescas.py")
        if st.button('Produção de Solos'):
            st.switch_page("pages/producao_solos.py")
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
