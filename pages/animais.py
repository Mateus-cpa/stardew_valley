import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
    if st.button('Home'):
        st.switch_page("../dataviz.py")
    # Carregar os dados
    animais = pd.read_csv('docs_silver/animais.csv', encoding='utf-8')
    animais = animais.drop(columns=['Unnamed: 0'])

    # Título
    st.title('Animais')
    
    custo_animais = animais.Custo.mean()
    valor_produtos = round(animais.Produz_valor.mean())

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Tamanho da tabela', animais.shape[0])
        st.metric('Quantidade de colunas', animais.shape[1])
        
    with col2:
        st.metric('Custo médio de animais', custo_animais)
        st.metric('Valor médio dos produtos', valor_produtos)
        
    with col3:
        st.metric('Rendimento por venda', round(animais['Rendimento de venda'].mean(), 2))
        st.metric('Rendimento médio de produção', round(animais['Rendimento de produção'].mean(), 2))

    st.dataframe(animais, 
                 hide_index=True, 
                 on_select='rerun',
                 selection_mode='multi-row')

    animais = animais.sort_values(by='Rendimento de produção', ascending=False).dropna(subset='Custo')

    st.subheader('Gráfico de rendimento de animais de produtos gerados')
    fig, ax = plt.subplots()
    # plotar rendimento de produção por nome
    animais.plot(kind='bar', ax=ax, x='Nome', y='Rendimento de produção')
    st.pyplot(fig)
    
    st.subheader('Gráfico de rendimento de produto por custo dos animais')
    fig, ax = plt.subplots()
    # Agrupar por 'Produz_item' e calcular a média de 'Rendimento de produção'
    animais_grouped = animais.groupby('Produz_item')['Rendimento de produção'].mean().reset_index()
    # Ordenar por 'Rendimento de produção'
    animais_grouped = animais_grouped.sort_values(by='Rendimento de produção', ascending=False)
    # plotar rendimento de produção por item produzido
    animais_grouped.plot(kind='bar', ax=ax, x='Produz_item', y='Rendimento de produção')
    st.pyplot(fig)

if __name__ == '__main__':
    main()