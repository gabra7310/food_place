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
from geopy.distance   import geodesic
from folium.plugins   import MarkerCluster

# =========================
# Helper dicts
# =========================

COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}

price_range = {
1:'cheap',
2:'normal',
3:'expensive',
4:'gourmet',
}

COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}

rating_text_pt = {
    'Excellent':'Excelente',
    'Very Good':'Muito bom', 
    'Good':'Bom',
    'Average':'Regular',
    'Not rated':'Não avaliado',
    'Poor':'Ruim',
    'Vynikajúce':'Excelente',
    'Bardzo dobrze':'Muito bom',
    'Muy Bueno':'Muito bom',
    'Bueno':'Bom',
    'Baik':'Bom',
    'Biasa':'Regular',
    'Skvělá volba':'Excelente',
    'Velmi dobré':'Muito bom',
    'Buono':'Bom',
    'Skvělé':'Excelente',
    'Wybitnie':'Excelente',
    'Sangat Baik': 'Muito bom',
    'Terbaik':'Excelente',
    'İyi':'Bom',
    'Excelente':'Excelente',
    'Muito bom':'Muito bom',
    'Muito Bom':'Muito Bom',
    'Bom':'Bom',
    'Harika':'Excelente',
    'Çok iyi':'Muito bom',
    'Eccellente':'Excelente',
    'Veľmi dobré':'Muito bom',
}

currency_values = {'Botswana Pula(P)': 0.068, 
                   'Brazilian Real(R$)': 0.164, 
                   'Dollar($)': 1.0, 
                   'Emirati Diram(AED)': 0.27, 
                   'Indian Rupees(Rs.)': 0.013, 
                   'Indonesian Rupiah(IDR)': 0.000069, 
                   'NewZealand($)': 0.684, 
                   'Pounds(£)': 1.388, 
                   'Qatari Rial(QR)': 0.27, 
                   'Rand(R)': 0.066, 
                   'Sri Lankan Rupee(LKR)': 0.005, 
                   'Turkish Lira(TL)': 0.118}

binary = {0:'Não', 1:'Sim'}

# =========================
# Helper functions
# =========================

def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

def load_dataset():
    df = pd.read_csv('data/zomato.csv')
    return df

def clean_data (df):
    df = rename_columns(df)

    # Drop switch_to_order_menu - only 0 values
    df = df.drop(columns=['switch_to_order_menu'], axis=1)

    # Drop duplicates in considering the restaurant id, keeping the first ones
    df = df.drop_duplicates(subset=['restaurant_id'], keep='first')

    # Drop NA
    df = df.dropna()

    return df

def feature_engineering(df):

    # Mapping the column country_code to contry name
    df['country'] = df['country_code'].map(COUNTRIES)

    # Creating price type
    df['price_type'] = df['price_range'].map(price_range)

    # Changing the rating color
    df['rating_color'] = df['rating_color'].map(COLORS)

    # Only consider the first type of cousine
    df["cuisines"] = df.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])


    # Change the binary columns to yes or no
    df['has_table_booking'] = df['has_table_booking'].map(binary)
    df['has_online_delivery'] = df['has_online_delivery'].map(binary)
    df['is_delivering_now'] = df['is_delivering_now'].map(binary)

    # Change the rating text - normalizing for all languages
    df['rating_text_pt'] = df['rating_text'].map(rating_text_pt).str.title()

    # Convert cost to dollar - normalazing currency
    df['convert_dol'] = df.loc[:, 'currency'].map(currency_values)
    df['avg_cost_dol'] = df['average_cost_for_two'] * df['convert_dol']

    # Dropping columns that will not be used
    drop = ['country_code', 'price_range', 'rating_text', 'convert_dol']
    df = df.drop(columns=drop, axis=1)

    return df

def create_map(df):
    cols = ['rating_color', 'restaurant_name', 'average_cost_for_two', 'avg_cost_dol', 'cuisines', 'aggregate_rating', 'longitude', 'latitude', 'currency']
    df_aux = df.loc[:, cols].reset_index()

    df_aux1 = df_aux.loc[:, ['latitude', 'longitude']].values.tolist()

    map = folium.Map()

    cluster = MarkerCluster().add_to(map)

    for index, location_info in df_aux.iterrows():
        html = """<b>"""+ location_info['restaurant_name'] + """</b>
        <p>
        Price (local currency): <b>""" + str(np.round(location_info['average_cost_for_two'],2)) + """ """ + str(location_info['currency']) + """</b> for two
        </br>
        Price (US$ dol.): <b>""" + str(np.round(location_info['avg_cost_dol'],2)) + """</b> for two
        </br>
        Cuisine: <b>""" + location_info['cuisines'] + """</b>
        </br>
        Aggragate Rating: <b>""" + str(location_info['aggregate_rating']) + """/5.0</b>
        </p>
        """ 
        #iframe = folium.IFrame(html,width=100,height=100)

        popup = folium.Popup(html, max_width=300)

        folium.Marker(
            [ location_info['latitude'], location_info['longitude'] ],
            popup=popup,
            icon=folium.Icon(color=location_info['rating_color'], icon='home') ).add_to(cluster)

    return map

def create_graph(df, col1, col2, method, label1, label2):
    cols = [col1, col2]
    
    if method == 'count':
        df_aux = df.loc[:, cols].groupby(cols[1]).count().reset_index().sort_values(cols[0], ascending=False)
        fig = px.bar(df_aux, x=col2, y=col1, color=col2, labels={col1:label1, col2:label2}, text_auto=True)
    
    if method == 'nunique':
        df_aux = df.loc[:, cols].groupby(cols[1]).nunique().reset_index().sort_values(cols[0], ascending=False)
        fig = px.bar(df_aux, x=col2, y=col1, color=col2, labels={col1:label1, col2:label2}, text_auto=True)        

    if method == 'mean':
        df_aux = df.loc[:, cols].groupby(cols[1]).mean().reset_index().sort_values(cols[0], ascending=False)
        fig = px.bar(df_aux, x=col2, y=col1, color=col2, labels={col1:label1, col2:label2}, text_auto=True)        

    return fig

def get_best_restaurant(df, cuisine_metric):
    cols = ['restaurant_name', 'aggregate_rating', 'restaurant_id', 'country', 'city', 'average_cost_for_two', 'currency']
    cond = df['cuisines'] == cuisine_metric
    df_aux = df.loc[cond,cols].sort_values(cols[1:3], ascending=[False,True]).reset_index()

    rest = cuisine_metric + ': ' + df_aux['restaurant_name'][0]
    rating = str(df_aux['aggregate_rating'][0]) + '/5.0'
    help = """
    País: """+ df_aux['country'][0] +"""

    Cidade: """ + df_aux['city'][0] + """ 

    Média Prato para dois: """ + str(df_aux['average_cost_for_two'][0]) + """ """ + df_aux['currency'][0]


    return rest, rating, help

def get_10_rest_rating(df, op, rating):
    cols = ['city', 'restaurant_id', 'country']

    if op == 'maior':
            cond = df['aggregate_rating'] >= rating

    if op == 'menor':
            cond = df['aggregate_rating'] <= rating

    df_aux = df.loc[cond, cols].groupby([cols[0], cols[2]]).count().reset_index().sort_values(cols[1], ascending=False)
    df_aux = df_aux.iloc[:11,:]

    fig = px.bar(df_aux, x=cols[0], y=cols[1], color=cols[2], labels={cols[0]:'Cidade', cols[1]:'Quantidade de restaurantes', cols[2]:'País'}, text_auto=True)

    return fig

def get_city_cuisines(df):
    cols = ['cuisines', 'city', 'country']

    df_aux = df.loc[:,cols].groupby(cols[1:]).nunique().reset_index().sort_values(cols[0], ascending=False)
    df_aux = df_aux.loc[:11,:]

    fig = px.bar(df_aux, x=cols[1], y=cols[0], color=cols[2], labels={cols[0]: 'Quantidade de restaurantes', cols[1]: 'Cidade', cols[2]: 'País'}, text_auto=True)

    return fig

def get_city_restaurants(df):
    cols = ['restaurant_id', 'city', 'country']
        
    df_aux = df.loc[:, cols].groupby(cols[1:]).count().reset_index().sort_values(cols[0], ascending=False)
    df_aux = df_aux.iloc[:11,:]

    fig = px.bar(df_aux, x=cols[1], y=cols[0], color='country', labels={cols[0]:'Quantidade de restaurantes', cols[1]:'Cidade', cols[2]:'País'}, text_auto=True)

    return fig

def center_text(title):
    title = "<p style='text-align: center; font-weight: bold;'>" + title + "</p>"
    return title

def get_top_cuisines(df, cond, qtd_rest):
    if cond == 'melhor':
        order = False
    if cond == 'pior':
        order = True

    cols = ['cuisines', 'aggregate_rating']
    df_aux = df.loc[:, cols].groupby(cols[0]).mean().reset_index().sort_values(cols[1], ascending=order)
    df_aux = df_aux.iloc[:qtd_rest, :]
    df_aux = df_aux.round(2)

    fig = px.bar(df_aux, x=cols[0], y=cols[1], labels={cols[0]:'Tipo de Culinária', cols[1]:'Média de Avaliação'}, text_auto=True)

    return fig

def get_top_restaurants(df, qtd_rest):
    cols = ['restaurant_id', 'restaurant_name', 'country', 'city', 'cuisines', 'average_cost_for_two', 'aggregate_rating', 'votes']
    df_aux = df.loc[:, cols].sort_values(['aggregate_rating', 'restaurant_id'], ascending=[False, True])
    df_aux = df_aux.iloc[:qtd_rest,:]

    return df_aux