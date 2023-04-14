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
    page_title = "🍽️ Cozinhas",
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
st.sidebar.image(image, width=60)

#st.sidebar.markdown('# Food Place')
#st.sidebar.markdown('## The best choices for your meal')

#st.sidebar.markdown("""---""")
st.sidebar.markdown('## Filtros')
country_option = st.sidebar.multiselect(
    'Selecione os países',
    df1['country'].unique(),
    default = ['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia']
)

qtd_rest = st.sidebar.slider(
    'Selecione a quantidade de restaurantes para visualizar', 0, 20, 10
)

cuisine_type = st.sidebar.multiselect(
    'Escolha os tipos de culinária',
    df1['cuisines'].unique(),
    default = ['Home-made', 'BBQ', 'Japanese', 'Brazilian', 'Arabian', 'American', 'Italian']
)

st.sidebar.markdown("""---""")
st.sidebar.markdown("Feito por Gabriel Alves - Comunidade DS")

# Dataset geral sem filtro - para métricas totais
df = df1.copy()

# Filtro de pais
filtro_cidade = df1['country'].isin(country_option)
df1 = df1.loc[filtro_cidade, :]

# Filtro de cuisine
filtro_cuisine = df1['cuisines'].isin(cuisine_type)
df1 = df1.loc[filtro_cuisine, :]




# =================================
# Main page
# =================================

st.write('# 🍽️ Visão Cozinhas')

with st.container():
    st.markdown(fp.center_text("Melhores Restaurantes dos principais tipos culinários"), unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        cuisine_metric = 'Italian'
        rest, rating, help = fp.get_best_restaurant(df, cuisine_metric)

        col1.metric(label=rest, value=rating, help=help)

    with col2:
        cuisine_metric = 'American'
        rest, rating, help = fp.get_best_restaurant(df, cuisine_metric)

        col2.metric(label=rest, value=rating, help=help)   
    
    with col3:
        cuisine_metric = 'Arabian'
        rest, rating, help = fp.get_best_restaurant(df, cuisine_metric)

        col3.metric(label=rest, value=rating, help=help)

    with col4:
        cuisine_metric = 'Japanese'
        rest, rating, help = fp.get_best_restaurant(df, cuisine_metric)
        
        col4.metric(label=rest, value=rating, help=help)

    with col5:
        cuisine_metric = 'Brazilian'
        rest, rating, help = fp.get_best_restaurant(df, cuisine_metric)
        
        col5.metric(label=rest, value=rating, help=help)

with st.container():
    st.markdown("""---""")
    st.markdown(fp.center_text("Top " + str(qtd_rest) + " Restaurantes"), unsafe_allow_html=True)

    df_aux = fp.get_top_restaurants(df1, qtd_rest)
    st.dataframe(df_aux, use_container_width=True)

with st.container():
    st.markdown("""---""")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(fp.center_text("Top " + str(qtd_rest) + " melhores tipos culinários"), unsafe_allow_html=True)

        fig = fp.get_top_cuisines(df, 'melhor', qtd_rest)
        st.plotly_chart(fig, use_container_width=True)

    
    with col2:
        st.markdown(fp.center_text("Top " + str(qtd_rest) + " piores tipos culinários"), unsafe_allow_html=True)

        fig = fp.get_top_cuisines(df, 'pior', qtd_rest)
        st.plotly_chart(fig, use_container_width=True)