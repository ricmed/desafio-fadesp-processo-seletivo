import streamlit as st
import pandas as pd
import plotly.express as px

# Importar os dados
path = './data/dataset_desafio_fadesp.csv'
df = pd.read_csv(path, encoding='ISO-8859-1', sep=',')

# Converte 'Order Date' para datetime e extrai o mês e o ano
# Convertendo as colunas para os tipos corretos
df['Order Date'] = df['Order Date'].str.replace('-','/')
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')

df['YearMonth'] = df['Order Date'].dt.to_period('M')

df = df.drop(columns=['Row ID', 'Customer ID', 'Customer Name', 'Product ID', 'Postal Code'])
colunas_categoricas = df.select_dtypes(include= 'object').columns

def convert_categoria(df: pd.DataFrame, colunas):
    for coluna in colunas:
        df[coluna] = df[coluna].astype('category')
    return df

df = convert_categoria(df, colunas_categoricas)

# Converte 'Order Date' para datetime e extrai o mês e o ano
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['YearMonth'] = df['Order Date'].dt.to_period('M')

# Cria os filtros
selected_segment = st.selectbox('Segment', df['Segment'].unique())
selected_region = st.selectbox('Region', df['Region'].unique())
selected_category = st.selectbox('Category', df['Category'].unique())
#selected_priority = st.selectbox('Order Priority', df['Order Priority'].unique())
selected_yearmonth = st.selectbox('Year-Month', df['YearMonth'].unique())

# Filtra o DataFrame com base nos filtros selecionados
filtered_df = df[(df['Segment'] == selected_segment) &
                 (df['Region'] == selected_region) &
                 (df['Category'] == selected_category) &
                 #(df['Order Priority'] == selected_priority) &
                 (df['YearMonth'] == selected_yearmonth)]

# Cria os gráficos
sales_date_figure = px.line(filtered_df, x='Order Date', y='Sales')
sales_region_figure = px.bar(filtered_df, x='Region', y='Sales')
sales_profit_figure = px.scatter(filtered_df, x='Sales', y='Profit')

# Exibe os gráficos
st.plotly_chart(sales_date_figure)
st.plotly_chart(sales_region_figure)
st.plotly_chart(sales_profit_figure)