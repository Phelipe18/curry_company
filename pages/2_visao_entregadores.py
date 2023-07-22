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

st.header('Marketplace - Visão Entregadores')

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
     value = datetime(2022, 4, 13),
     min_value = datetime(2022, 2, 11 ),
     max_value = datetime(2022, 4, 6 ),
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

# Linkando o Filtro do Trânsito
linhas_selecionadas = df['Road_traffic_density'].isin(traffic_options)
df = df.loc[linhas_selecionadas, :]

#==============================
#Layout Streamlit
#==============================

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '_', '_'])

with tab1:
    with st.container():
        st.title('Overall Metrics')
        
        col1, col2, col3, col4 = st.columns(4, gap='large')
        with col1:
            maior_idade = df.loc[:, 'Delivery_person_Age'].max()         
            col1.metric('Maior Idade', maior_idade)
            
        with col2:
            menor_idade = df.loc[:, 'Delivery_person_Age'].min()
            col2.metric('Menor Idade', menor_idade)
            
        with col3:
            melhor_condi = df.loc[:, 'Vehicle_condition'].max()
            col3.metric('Melhor condição', melhor_condi)
            
        with col4:
            pior_condi = df.loc[:,'Vehicle_condition'].min()
            col4.metric('Pior condição', pior_condi)
            
    with st.container():
        st.markdown("""---""")
        st.title('Ratings')
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Av. média por entregador')
            cols = ['Delivery_person_Ratings', 'Delivery_person_ID']
            df_aux = df.loc[:, cols].groupby(['Delivery_person_ID']).mean().reset_index()
            st.dataframe(df_aux)
            
        with col2:
            st.subheader('Av. média por trânsito')
            cols = ['Delivery_person_Ratings', 'Road_traffic_density']
            df_aux = df.loc[:, cols].groupby(['Road_traffic_density']).agg({'Delivery_person_Ratings': [ 'mean', 'std' ]})
            df_aux.columns = ['delivery_mean', 'delivery_std']
            df_aux = df_aux.reset_index()
            st.dataframe(df_aux)
            
            st.subheader('Av. média por clima')
            cols = ['Delivery_person_Ratings', 'Weatherconditions']
            df_aux = df.loc[:, cols].groupby(['Weatherconditions']).agg({'Delivery_person_Ratings': [ 'mean', 'std' ]})
            df_aux.columns = ['delivery_mean', 'delivery_std']
            df_aux = df_aux.reset_index()
            st.dataframe(df_aux)
    
    with st.container():
        st.markdown("""---""")
        st.title('Velocidade de Entrega')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader('Entregadores mais rápidos')
            df2 = df.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']].groupby(['City', 'Delivery_person_ID']).min().sort_values(['City',                 'Time_taken(min)'], ascending=True).reset_index()
            df_aux1 = df2.loc[df2['City'] == 'Metropolitian'].head(10)
            df_aux2 = df2.loc[df2['City'] == 'Urban'].head(10)
            df_aux3 = df2.loc[df2['City'] == 'Semi-Urban'].head(10)
            df_rapid = pd.concat( [df_aux1, df_aux2, df_aux3] ).reset_index(drop=True)
            st.dataframe(df_rapid)
        
        with col2:
            st.subheader('Entregadores mais lentos')
            df2 = df.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']].groupby(['City', 'Delivery_person_ID']).max().sort_values(['City',                 'Time_taken(min)'], ascending=False).reset_index()
            df_aux1 = df2.loc[df2['City'] == 'Metropolitian'].head(10)
            df_aux2 = df2.loc[df2['City'] == 'Urban'].head(10)
            df_aux3 = df2.loc[df2['City'] == 'Semi-Urban'].head(10)
            df_lento = pd.concat( [df_aux1, df_aux2, df_aux3] ).reset_index(drop=True)
            st.dataframe(df_lento)
