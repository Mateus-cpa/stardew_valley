import streamlit as st
import pandas as pd
import altair as alt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  # Carregar os dados
  lavoura = pd.read_csv('docs_silver/lavouras.csv',encoding='utf-8').iloc[:,1:]
  lavoura['Semente_original'] = lavoura['Semente'].apply(lambda x: x.split('_')[0])
 

  # Título
  st.title('Lavoura')

  #Filtros
  col1, col2 = st.columns(2)
  filtro_estacao = col1.multiselect('Estação', lavoura['Estação'].unique())
  if filtro_estacao:
    lavoura = lavoura[lavoura['Estação'].isin(filtro_estacao)]
  filtro_texto = col2.text_input('Filtre por um termo:', '')
  if filtro_texto:
    lavoura = lavoura[lavoura['Semente'].str.contains(filtro_texto, case=False)]
  
  #KPIs
  col1, col2, col3 = st.columns(3)
  col1.metric('Qtde. resultados', lavoura.shape[0])
  col2.metric('Valor Venda (média)', round(lavoura['Vende_por'].mean(),2))
  col3.metric('Saúde (média)', round(lavoura['Saude'].mean(),2))
  col3.metric('Energia(média)', round(lavoura['Energia'].mean(),2))
  col2.metric('Renda média (ouro por dia)', round(lavoura['Renda média (ouro por dia)'].mean(),2))
  col1.metric('Crescimento (dias)', round(lavoura['Crescimento Total (dias)'].mean(),2))
  
  st.write(lavoura, use_container_width=True,hide_index=True)
  
  # Paleta de cores mapeada para cada estação
  paleta_estacoes = {
    'Especial': 'white',  # Branco
    'Outono': 'brown',    # Marrom Avermelhado
    'Primavera': 'lightgreen', # Verde Menta
    'Verão': 'gold'}     # Verde Limão
  # Cria a coluna 'Cor' usando map e get para cor padrão
  lavoura['Cor'] = lavoura['Estação'].map(lambda x: paleta_estacoes.get(x, 'gray'))

  if not filtro_estacao:
    # Gráfico de quantidade de resultados por estação
    grafico_quant = alt.Chart(lavoura).mark_bar().encode(
        x=alt.X('Estação:N', title='Estação'),
        y=alt.Y('count():Q', title='Quantidade de resultados'),
        color=alt.Color('Cor:N', scale=None),
        tooltip=['Estação', 'count()']
    ).properties(
        title='Quantidade de resultados por estação',
        width=alt.Step(80))  # Largura das barras
    media_quantidade = lavoura.groupby('Estação').size().mean()
    linha_media_quant = alt.Chart(pd.DataFrame({'Média': [media_quantidade]})).mark_rule(color='gray', bandSize=10).encode(
        y='Média:Q')
    grafico_quant = grafico_quant + linha_media_quant
    
    # gráfico de média de valor de venda por estação
    grafico_venda = alt.Chart(lavoura).mark_bar().encode(
        x=alt.X('Estação:N', title='Estação'),
        y=alt.Y('mean(Vende_por):Q', title='Valor de venda médio'),
        color=alt.Color('Cor:N', scale=None),
        tooltip=['Estação', 'mean(Vende_por)']
    ).properties(
        title='Valor de venda médio por estação',
        width=alt.Step(80))  # Largura das barras
    media_venda = lavoura['Vende_por'].mean()
    linha_media_venda = alt.Chart(pd.DataFrame({'Média': [media_venda]})).mark_rule(color='gray', bandSize=10).encode(
        y='Média:Q')
    grafico_venda = grafico_venda + linha_media_venda

    grafico_saude = alt.Chart(lavoura).mark_bar().encode(
        x=alt.X('Estação:N', title='Estação'),
        y=alt.Y('mean(Saude):Q', title='Saúde média'),
        color=alt.Color('Cor:N', scale=None),
        tooltip=['Estação', 'mean(Saude)']
    ).properties(
        title='Saúde média por estação',
        width=alt.Step(80))  # Largura das barras
    media_saude = lavoura['Saude'].mean()
    linha_media_saude = alt.Chart(pd.DataFrame({'Média': [media_saude]})).mark_rule(color='gray', bandSize=10).encode(
        y='Média:Q')
    grafico_saude = grafico_saude + linha_media_saude
    
    grafico_energia = alt.Chart(lavoura).mark_bar().encode(
        x=alt.X('Estação:N', title='Estação'),
        y=alt.Y('mean(Energia):Q', title='Energia média'),
        color=alt.Color('Cor:N', scale=None),
        tooltip=['Estação', 'mean(Energia)']
    ).properties(
        title='Energia média por estação',
        width=alt.Step(80))  # Largura das barras
    media_quantidade = lavoura['Energia'].mean()
    linha_media_quant = alt.Chart(pd.DataFrame({'Média': [media_quantidade]})).mark_rule(color='gray', bandSize=10).encode(
        y='Média:Q')
    grafico_energia = grafico_energia + linha_media_quant

    # gráfico de barra poe estação da coluna Renda média (ouro por dia)
    grafico_ouro_dia = alt.Chart(lavoura).mark_bar().encode(
        x=alt.X('Estação:N', title='Estação'),
        y=alt.Y('mean(Renda média (ouro por dia)):Q', title='Renda média'),
        color=alt.Color('Cor:N', scale=None),
        tooltip=['Estação', 'mean(Renda média (ouro por dia))']
    ).properties(
        title='Preço médio por estação',
        width=alt.Step(80))  # Largura das barras
    media_ouro_dia = lavoura['Renda média (ouro por dia)'].mean()
    linha_media_ouro_dia = alt.Chart(pd.DataFrame({'Média': [media_ouro_dia]})).mark_rule(color='gray', bandSize=10).encode(
        y='Média:Q')
    grafico_ouro_dia = grafico_ouro_dia + linha_media_ouro_dia

    grafico_crescimento = alt.Chart(lavoura).mark_bar().encode(
        x=alt.X('Estação:N', title='Estação'),
        y=alt.Y('mean(Crescimento Total (dias)):Q', title='Crescimento médio'),
        color=alt.Color('Cor:N', scale=None),
        tooltip=['Estação', 'mean(Crescimento Total (dias))']
    ).properties(
        title='Crescimento médio por estação',
        width=alt.Step(80))  # Largura das barras
    media_crescimento = lavoura['Crescimento Total (dias)'].mean()
    linha_media_crescimento = alt.Chart(pd.DataFrame({'Média': [media_crescimento]})).mark_rule(color='gray', bandSize=10).encode(
        y='Média:Q')
    grafico_crescimento = grafico_crescimento + linha_media_crescimento
    
    # Exibe o gráfico no Streamlit
    col1, col2 = st.columns(2)
    col1.altair_chart(grafico_quant, use_container_width=True)
    col2.altair_chart(grafico_venda, use_container_width=True)
    col1.altair_chart(grafico_saude, use_container_width=True)
    col2.altair_chart(grafico_energia, use_container_width=True)
    col1.altair_chart(grafico_ouro_dia, use_container_width=True)
    col2.altair_chart(grafico_crescimento, use_container_width=True)
  #gráficos scatter com else (filtro ativo)
  else:
    #plotar gráfico scatter utilizando renda média como tamanho
    grafico_scatter = alt.Chart(lavoura).mark_point().encode(
      x='Renda média (ouro por dia)',
      y='Crescimento Total (dias)',
      size='Energia',
      color = 'Saude',
      tooltip=['Semente','Energia','Saude','Renda média (ouro por dia)','Crescimento Total (dias)']).properties(
    width=800,
    height=400)
    st.altair_chart(grafico_scatter)
    
  # fim da função

  

if __name__ == '__main__':
    main()
