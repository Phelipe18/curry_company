import pandas as pd
import plotly.express as px
import io
from PIL import Image
import streamlit as st
from streamlit_folium import folium_static
import folium
from datetime import datetime


df = pd.read_csv( 'dataset/train.csv' )

# Limpeza de arquivo
linhas_vazias = df['ID'] != 'NaN '
df = df.loc[linhas_vazias, :]
linhas_vazias = df['Delivery_person_ID'] != 'NaN '
df = df.loc[linhas_vazias, :]
linhas_vazias = df['Delivery_person_Age'] != 'NaN '
df = df.loc[linhas_vazias, :]
linhas_vazias = df['Delivery_person_Ratings'] != 'NaN '
df = df.loc[linhas_vazias, :]
linhas_vazias = df['Restaurant_latitude'] != 'NaN '
df = df.loc[linhas_vazias, :]
linhas_vazias = df['Restaurant_longitude'] != 'NaN '
df = df.loc[linhas_vazias, :]
linhas_vazias = df['Delivery_location_latitude'] != 'NaN '
df = df.loc[linhas_vazias, :]
linhas_vazias = df['Delivery_location_longitude'] != 'NaN '
df = df.loc[linhas_vazias, :]
linhas_vazias = df['Order_Date'] != 'NaN '
df = df.loc[linhas_vazias, :]
linhas_vazias = df['Time_Order_picked'] != 'NaN '
df = df.loc[linhas_vazias, :]
linhas_vazias = df['Weatherconditions'] != 'conditions NaN'
df = df.loc[linhas_vazias, :]
linhas_vazias = df['Vehicle_condition'] != 'NaN '
df = df.loc[linhas_vazias, :]
linhas_vazias = df['Type_of_order'] != 'NaN '
df = df.loc[linhas_vazias, :]
linhas_vazias = df['Type_of_vehicle'] != 'NaN '
df = df.loc[linhas_vazias, :]
linhas_vazias = df['multiple_deliveries'] != 'NaN '
df = df.loc[linhas_vazias, :]
linhas_vazias = df['Festival'] != 'NaN '
df = df.loc[linhas_vazias, :]
linhas_vazias = df['City'] != 'NaN '
df = df.loc[linhas_vazias, :]
linhas_vazias = df['Time_taken(min)'] != 'NaN '
df = df.loc[linhas_vazias, :]

#Retirando o min do time.
df['Time_taken(min)'] = df['Time_taken(min)'].apply( lambda x: x.split( '(min) ')[1])

# Reset index
df = df.reset_index( drop=True )

#Mudança de tipo
df['Delivery_person_Age'] = df['Delivery_person_Age'].astype( int )
df['multiple_deliveries'] = df['multiple_deliveries'].astype( int )
df['Delivery_person_Ratings'] = df['Delivery_person_Ratings'].astype( float )
df['Order_Date'] = pd.to_datetime( df['Order_Date'], format='%d-%m-%Y' )
df['Time_taken(min)'] = df['Time_taken(min)'].astype(int)

# Espaço na string
df.loc[:, 'ID'] = df.loc[:, 'ID'].str.strip()
df.loc[:, 'Delivery_person_ID'] = df.loc[:, 'Delivery_person_ID'].str.strip()
df.loc[:, 'Time_Orderd'] = df.loc[:, 'Time_Orderd'].str.strip()
df.loc[:, 'Time_Order_picked'] = df.loc[:, 'Time_Order_picked'].str.strip()
df.loc[:, 'Weatherconditions'] = df.loc[:, 'Weatherconditions'].str.strip()
df.loc[:, 'Road_traffic_density'] = df.loc[:, 'Road_traffic_density'].str.strip()
df.loc[:, 'Type_of_order'] = df.loc[:, 'Type_of_order'].str.strip()
df.loc[:, 'Type_of_vehicle'] = df.loc[:, 'Type_of_vehicle'].str.strip()
df.loc[:, 'Festival'] = df.loc[:, 'Festival'].str.strip()
df.loc[:, 'City'] = df.loc[:, 'City'].str.strip()


#==============================
#Barra Lateral
#==============================

st.header('Marketplace - Visão Cliente')

#Imagem
image = Image.open('logo.jpg')
st.sidebar.image(image, width= 120 )

#Sidebar
st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

#Filtro
st.sidebar.markdown('## Selecione uma data limite')
date_slider = st.sidebar.slider(
    'Até qual valor?',
     value = pd.datetime(2022, 4, 13),
     min_value = pd.datetime(2022, 2, 11 ),
     max_value = pd.datetime(2022, 4, 6 ),
     format='DD-MM-YYYY')

st.sidebar.markdown("""---""")
# Filtro
traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito?',
    ['Low','Medium','High','Jam'],
    default = ['Low','Medium','High','Jam'])
st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powered by Comunidade DS')

# Linkando o Filtro de Data
linhas_selecionadas = df['Order_Date'] < date_slider
df = df.loc[linhas_selecionadas, :]
st.dataframe(df.head())

# Linkando o Filtro do Trânsito
linhas_selecionadas = df['Road_traffic_density'].isin(traffic_options)
df = df.loc[linhas_selecionadas, :]

#==============================
#Layout Streamlit
#==============================

tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container():
        # Order Metric
        st.markdown('# Orders by Day')
        # 1. Quantidade de pedidos por dia. No gráfico de barras.
        cols = ['ID', 'Order_Date']
        df_aux = df.loc[:, cols].groupby(['Order_Date']).count().reset_index()
        fig = px.bar(df_aux, x='Order_Date', y='ID')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('#Teste 01')
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.header('Traffic Order Share')
            cols = ['ID', 'Road_traffic_density']
            df_aux = df.loc[:, cols].groupby(['Road_traffic_density']).count().reset_index()
            fig = px.pie(df_aux, names='Road_traffic_density', values='ID')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.header('Traffic Order City')
            cols = ['ID', 'City', 'Road_traffic_density']
            df_aux = df.loc[:, cols].groupby(['City', 'Road_traffic_density']).count().reset_index()
            fig = px.bar(df_aux, x='City', y='Road_traffic_density', color='Road_traffic_density', barmode='group', text_auto=True)
            st.plotly_chart(fig, use_container_width=True)
            
with tab2:
    with st.container():
        st.markdown('# Order by Week')
        df['week_of_year'] = df['Order_Date'].dt.strftime('%U')
        cols = ['week_of_year', 'ID']
        df_aux = df.loc[:, cols].groupby(['week_of_year']).count().reset_index()
        fig = px.line(df_aux, x='week_of_year', y='ID')
        st.plotly_chart(fig, use_container_width=True)
        
    with st.container():
        st.markdown('# Order Share by Week')
        df_aux1 = df.loc[:, ['ID', 'week_of_year']].groupby(['week_of_year']).count().reset_index()
        df_aux2 = df.loc[:, ['Delivery_person_ID','week_of_year']].groupby(['week_of_year']).nunique().reset_index()
        df_aux3 = pd.merge(df_aux1, df_aux2, how='inner')
        df_aux3["order_by_delivery"] = df_aux3["ID"] / df_aux3["Delivery_person_ID"]
        fig = px.line(df_aux3, x='week_of_year', y='order_by_delivery')
        st.plotly_chart(fig, use_container_width=True)
        
with tab3:
    st.markdown('# Country Maps')
    cols = ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']
    df_aux = df.loc[:, cols].groupby(['City', 'Road_traffic_density']).median().reset_index()
    # Tenho que importar o folium para tirar o #, dando pip install.
    map = folium.Map()
    for index, location_info in df_aux.iterrows():
        folium.Marker( [location_info['Delivery_location_latitude'],
                        location_info['Delivery_location_longitude']]).add_to(map)
    # Tem que usar o from streamlit_folium import folium_static
    folium_static(map, width=1024, height=600)
    

        
    
