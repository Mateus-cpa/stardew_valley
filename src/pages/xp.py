import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
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

