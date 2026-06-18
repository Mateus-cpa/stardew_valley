import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
    if st.button('Home'):
        st.switch_page("dataviz.py")
    # Carregar os dados
    armas = pd.read_csv('docs_silver/armas.csv', encoding='utf-8')
    # Retirar primeira coluna
    armas = armas.iloc[:, 1:]
    
    # Título
    st.title('Armas')
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Tamanho da tabela', armas.shape[0])
    with col2:
        st.metric('Quantidade de colunas', armas.shape[1])
    with col3:
        st.metric('Dano médio', round(armas['Dano médio'].mean(), 2))
    with col4:
        st.metric('Valor de arma por dano médio', round(armas['Valor por dano'].mean(), 2))
    
    # Exibir dataframe com a quantidade de linhas selecionada
    st.dataframe(armas, hide_index=True)
    
    # Slider para selecionar a quantidade de linhas a serem exibidas
    num_linhas = st.slider('Quantidade de linhas a serem exibidas', min_value=1, max_value=armas.shape[0], value=armas.shape[0])
    ascending = st.checkbox('Crescente', value=False)
    df_armas_filtrada = armas.sort_values(by='Dano médio', ascending=ascending).head(num_linhas)

    col5, col6 = st.columns(2)

    with col5:
        st.metric('Dano médio', round(df_armas_filtrada['Dano médio'].mean(), 2))
        
        # Gráfico de dano
        fig, ax = plt.subplots()
        df_armas_filtrada.plot(kind='bar', ax=ax, x='Nome', y='Dano médio', grid=True)
        st.pyplot(fig)

    with col6:
        st.metric('Valor de arma por dano médio', round(armas['Valor por dano'].dropna().head(num_linhas).mean(), 2))
    
        # Gráfico de valor por dano
        fig, ax = plt.subplots()
        armas.sort_values(by='Valor por dano', ascending=ascending).dropna(subset='Valor por dano').head(num_linhas).plot(kind='bar', ax=ax, x='Nome', y='Valor por dano', grid=True)
        st.pyplot(fig)

    # Exibir dataframe com a quantidade de linhas selecionada
    st.dataframe(df_armas_filtrada, hide_index=True)

if __name__ == '__main__':
    main()