import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
  if st.button('Home'):
    st.switch_page("dataviz.py")
  
  # Carregar os dados
  xp = pd.read_csv('docs_silver/xp.csv',encoding='utf-8')
  
  st.title('XP')
  def filter_dataframe(df, selected_values):
      if selected_values:
          filtered_df = df[df['Profissao'].isin(selected_values)]
      else:
          filtered_df = df
      return filtered_df

  selected_values = st.multiselect('Selecione filtro por Profissão:', xp['Profissao'].unique())# Create a multiselect widget for selecting values
  filtered_xp = filter_dataframe(xp, selected_values)# Filter the DataFrame based on selected values

  st.dataframe(filtered_xp)# Display the filtered DataFrame
  st.bar_chart(filtered_xp,x='item',
              y='XP',
              x_label='Item',
              y_label='Valor de Experiência',
              horizontal=True)

  
  
  # fim da função


if __name__ == '__main__':
    main()



"""def grafico_xp ():
  #xp cultivo
  sns.boxplot(data=df_xp_cultivos, y='Estacao', x='XP', hue='Estacao')

  df_xp_cultivos = df_xp_cultivos.sort_values(by='XP', ascending=False)
  with sns.axes_style('whitegrid'):
    grafico = sns.barplot(data=df_xp_cultivos, y='Cultivo', x='XP', hue='Estacao', width = 0.8)
    grafico.set_title('XP por cultivo')
    grafico.set_xlabel('XP')
    grafico.set_ylabel('Cultivo')
    #tamanho do gráfico
    grafico.figure.set_size_inches(10, 20)
    
  #qualidade cultivo
  #fixar cores da legenda
  
  pass
  """