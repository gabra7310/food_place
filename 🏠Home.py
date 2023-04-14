# =========================
# Imports
# =========================

import pandas    as pd
import numpy     as np
import streamlit as st
import folium
import inflection

import plotly.express       as px
import plotly.graph_objects as go

from PIL              import Image
from streamlit_folium import folium_static
from streamlit_folium import st_folium
from geopy.distance   import geodesic

import src.foodplace as fp

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title = "🏠 Home",
    page_icon = "🍝",
    layout='wide'
)

# =================================
# ETL
# =================================

# Load dataset
df = fp.load_dataset()

# Clean dataset
df1 = fp.clean_data(df)

# Feature engineering
df1 = fp.feature_engineering(df1)

# =================================
# Sidebar
# =================================

image = Image.open('img/logo.png')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Food Place')
st.sidebar.markdown('## The best choices for your meal')

st.sidebar.markdown("""---""")
st.sidebar.markdown('## Filtros')
country_option = st.sidebar.multiselect(
    'Selecione os países',
    df1['country'].unique(),
    default = ['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia']
)

st.sidebar.markdown("""---""")
st.sidebar.markdown("Feito por Gabriel Alves - Comunidade DS")

# Dataset geral sem filtro - para métricas totais
df = df1.copy()

# Filtro de pais
filtro_cidade = df1['country'].isin(country_option)
df1 = df1.loc[filtro_cidade, :]



# =================================
# Main page
# =================================

st.write('# Food Place - The best choices for your meal')

st.markdown(""" 
## O Melhor lugar para encontrar seu mais novo restaurante favorito!
### Dentro desse dashboard você vai encontrar as seguintes marcas:
""")

#Container com as métricas gerais do dataset
with st.container():
    st.markdown("""---""")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        col1.metric(label='Restaurantes cadastrados', value=df['restaurant_id'].nunique())
    
    with col2:
        col2.metric(label='Países cadastrados', value=df['country'].nunique())
    
    with col3:
        col3.metric(label='Cidades cadastradas', value=df['city'].nunique())

    with col4:
        col4.metric(label='Avaliações na plataforma', value=df['votes'].sum())

    with col5:
        col5.metric(label='Culinárias oferecidas', value=df['cuisines'].nunique())


with st.container():
    #Cria  mapa interativo com os restaurantes registrados e filtrados na aba lateral
    
    folium_static(fp.create_map(df1), width=1024, height=600)