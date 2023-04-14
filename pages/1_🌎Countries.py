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
    page_title = "🌎 Countries",
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

st.write('# 🌎 Visão Países')

with st.container():
    st.markdown(fp.center_text("Quantidade de restaurantes  registrados por país"), unsafe_allow_html=True)
    
    fig = fp.create_graph(df1, 'restaurant_id', 'country', 'count', 'Quantidade de restaurantes', 'País')
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    st.markdown(fp.center_text("Quantidade de cidades  registrados por país"), unsafe_allow_html=True)
        
    fig = fp.create_graph(df1, 'city', 'country', 'nunique', 'Quantidade de cidades', 'País')
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        col1.markdown(fp.center_text("Média de avaliações feitas por país"), unsafe_allow_html=True)

        fig = fp.create_graph(df1, 'votes', 'country', 'mean', 'Média de avaliações', 'País')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        col2.markdown(fp.center_text("Média preço de um prato para duas pessoas por país"), unsafe_allow_html=True)

        fig = fp.create_graph(df1, 'avg_cost_dol', 'country', 'mean', 'Média preço (US$ dol)', 'País')
        st.plotly_chart(fig, use_container_width=True)

