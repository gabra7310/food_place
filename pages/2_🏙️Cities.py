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
    page_title = "🏙️ Cidades",
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

st.write('# 🌎 Visão Cidades')

with st.container():
    st.markdown(fp.center_text("Cidades com mais restaurantes cadastrados"), unsafe_allow_html=True)
        
    fig = fp.get_city_restaurants(df1)

    st.plotly_chart(fig, use_container_width=True)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(fp.center_text("Cidades com mais restaurantes de avaliação média acima de 4"), unsafe_allow_html=True)
        
        fig = fp.get_10_rest_rating(df1, 'maior', 4)

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown(fp.center_text("Cidades com mais restaurantes de avaliação média abaixo de 2.5"), unsafe_allow_html=True)

        fig = fp.get_10_rest_rating(df1, 'menor', 2.5)

        st.plotly_chart(fig, use_container_width=True)

with st.container():
    st.markdown(fp.center_text("Cidades com mais restaurantes com tipos culinários distintos"), unsafe_allow_html=True)
    
    fig = fp.get_city_cuisines(df1)

    st.plotly_chart(fig, use_container_width=True)


