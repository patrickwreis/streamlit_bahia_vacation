import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
from datetime import datetime

# Set page layout to wide
st.set_page_config(layout="wide", page_title="Viagem para Bahia 2024")

st.header('Viagem para Bahia 2024')
st.subheader('Gastos da Viagem')  # Corrigido erro de digitação

# Load dataframe
excel_file = 'feriass.xlsx'
sheet_name = 'Gasto'

df = pd.read_excel(excel_file, sheet_name=sheet_name)

# Ensure 'Data' column is in datetime format
df['Data'] = pd.to_datetime(df['Data'])
datas = df['Data'].unique().tolist()
min_data = df['Data'].min().date()
max_data = df['Data'].max().date()

nomes = df['Nome'].unique().tolist()
tipos = df['Tipo'].unique().tolist()
tipos_pagamentos = df['Tipo Pagamento'].unique().tolist()

data_selection = st.slider('Selecione a data', min_value=min_data, max_value=max_data, value=(min_data, max_data), format="DD/MM/YYYY")
data_selection = [datetime.combine(d, datetime.min.time()) for d in data_selection]  # Convert to datetime

tipo_selection = st.multiselect('Selecione o tipo', tipos, default=tipos)  # Corrigido erro de digitação
tipos_pagamentos_selection = st.multiselect('Selecione o tipo de pagamento', tipos_pagamentos, default=tipos_pagamentos)  # Corrigido erro de digitação

mask = (df['Data'].between(*data_selection)) & (df['Tipo'].isin(tipo_selection)) & (df['Tipo Pagamento'].isin(tipos_pagamentos_selection))
number_of_rows = df[mask].shape[0]

col1, col2 = st.columns(2)

# Gráfico de Barras: Total de gastos por tipo de gasto
with col1:
    df_grouped = df[mask].groupby('Tipo')['Valor'].sum().reset_index()  # Group by 'Tipo' and sum 'Valor'
    bar_chart = px.bar(df_grouped, x='Tipo', y='Valor', title='Total de Gastos por Tipo de Gasto', text_auto=True)
    bar_chart.update_traces(texttemplate='%{y:.2f}', textposition='outside')  # Add totals above bars
    st.plotly_chart(bar_chart)

# Gráfico de Linha: Gastos totais ao longo do tempo
with col1:
    line_chart = px.line(df[mask].groupby('Data')['Valor'].sum().reset_index(), x='Data', y='Valor', title='Gastos Totais ao Longo do Tempo')
    st.plotly_chart(line_chart)

# Gráfico de Pizza: Proporção de gastos por tipo de pagamento
with col2:
    pie_chart = px.pie(df[mask], names='Tipo Pagamento', values='Valor', title='Proporção de Gastos por Tipo de Pagamento')
    st.plotly_chart(pie_chart)

# Gráfico de Dispersão: Gastos em relação ao tempo
with col2:
    scatter_plot = px.scatter(df[mask], x='Data', y='Valor', color='Tipo', title='Gastos em Relação ao Tempo')
    st.plotly_chart(scatter_plot)