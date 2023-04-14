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

import foodplace as fp

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

image = Image.open('logo.png')
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
    st.markdown("<p style='text-align: center; font-weight: bold;'>Cidades com mais restaurantes cadastrados</p>", unsafe_allow_html=True)
    
    #fig = fp.create_graph(df1, 'restaurant_id', 'city', 'count', 'Quantidade de restaurantes', 'Cidade')
    cols = ['restaurant_id', 'city', 'country']
        
    df_aux = df1.loc[:, cols].groupby(cols[1:]).count().reset_index().sort_values(cols[0], ascending=False)
    df_aux = df_aux.loc[:10,:].sort_index()

    fig = px.bar(df_aux, x=cols[1], y=cols[0], color='country', labels={cols[0]:'Quantidade de restaurantes', cols[1]:'Cidade', cols[2]:'País'}, text_auto=True)
    
    st.plotly_chart(fig, use_container_width=True)
    #st.dataframe(df_aux)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<p style='text-align: center; font-weight: bold;'>Cidades com mais restaurantes de avaliação média acima de 4</p>", unsafe_allow_html=True)
        
        cols = ['city', 'restaurant_id', 'country']
        cond = df1['aggregate_rating'] >= 4

        df_aux = df1.loc[cond, cols].groupby([cols[0], cols[2]]).count().reset_index().sort_values(cols[1], ascending=False)
        df_aux = df_aux.loc[:7,:]

        fig = px.bar(df_aux, x=cols[0], y=cols[1], color=cols[2], labels={cols[0]:'Cidade', cols[1]:'Quantidade de restaurantes', cols[2]:'País'}, text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<p style='text-align: center; font-weight: bold;'>Cidades com mais restaurantes de avaliação média abaixo de 2.5</p>", unsafe_allow_html=True)
        cols = ['city', 'restaurant_id', 'country']
        cond = df1['aggregate_rating'] <= 2.5

        df_aux = df1.loc[cond, cols].groupby([cols[0], cols[2]]).count().reset_index().sort_values(cols[1], ascending=False)
        df_aux = df_aux.loc[0:6,:]

        fig = px.bar(df_aux, x=cols[0], y=cols[1], color=cols[2], labels={cols[0]:'Cidade', cols[1]:'Quantidade de restaurantes', cols[2]:'País'}, text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

with st.container():
    st.markdown("<p style='text-align: center; font-weight: bold;'>Cidades com mais restaurantes com tipos culinários distintos</p>", unsafe_allow_html=True)
    
    cols = ['cuisines', 'city', 'country']

    df_aux = df1.loc[:,cols].groupby(cols[1:]).nunique().reset_index().sort_values(cols[0], ascending=False)
    df_aux = df_aux.loc[:11,:]

    fig = px.bar(df_aux, x=cols[1], y=cols[0], color=cols[2], labels={cols[0]: 'Quantidade de restaurantes', cols[1]: 'Cidade', cols[2]: 'País'}, text_auto=True)
    st.plotly_chart(fig, use_container_width=True)


