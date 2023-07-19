import pandas as pd
import plotly.express as px
import io
from PIL import Image
import streamlit as st
from streamlit_folium import folium_static
import folium
import plotly.graph_objects as go

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

st.header('Marketplace - Visão Restaurantes')

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
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            delivery_unique = len(df.loc[:, 'Delivery_person_ID'].unique())
            col1.metric('Entregad. únicos', delivery_unique)
            
        with col2:
            st.title('2')
            cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
            #df['distance'] = df.loc[:, cols].apply(lambda x: haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'],                 #x['Delivery_location_longitude'])), axis=1)
            
        with col3:
            df_aux = (df.loc[:, ['Time_taken(min)', 'Festival']].groupby('Festival').agg({'Time_taken(min)':['mean', 'std']}))
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            df_aux = (df_aux.loc[df_aux['Festival'] == 'Yes', 'avg_time'])
            col3.metric('Time in Festival', df_aux)
            
        with col4:
            df_aux = (df.loc[:, ['Time_taken(min)', 'Festival']].groupby('Festival').agg({'Time_taken(min)':['mean', 'std']}))
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            df_aux = (df_aux.loc[df_aux['Festival'] == 'Yes', 'std_time'])
            col4.metric('STD in Festival', df_aux)
            
        with col5:
            df_aux = (df.loc[:, ['Time_taken(min)', 'Festival']].groupby('Festival').agg({'Time_taken(min)':['mean', 'std']}))
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            df_aux = (df_aux.loc[df_aux['Festival'] == 'No', 'avg_time'])
            col5.metric('Time not Festival', df_aux)
            
        with col6:
            df_aux = (df.loc[:, ['Time_taken(min)', 'Festival']].groupby('Festival').agg({'Time_taken(min)':['mean', 'std']}))
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            df_aux = (df_aux.loc[df_aux['Festival'] == 'No', 'std_time'])
            col6.metric('STD not Festival', df_aux)
            
            
    with st.container():
        st.markdown("""---""")
        st.title('Tempo médio de entrega por cidade')
        avg_distance = df.loc[:, ['City', 'Time_taken(min)']].groupby('City').mean().reset_index()
        fig = go.Figure( data=[ go.Pie( labels=avg_distance['City'], values=avg_distance['Time_taken(min)'], pull=[0, 0.1, 0])])
        st.plotly_chart(fig)
        
    with st.container():
        st.markdown("""---""")
        st.title('Distribuição do tempo')
        
        col1, col2 = st.columns(2)
        with col1:
            st.title('1')
        with col2:
            st.title('2')
       
        
    with st.container():
        st.markdown("""---""")
        st.title('Distribuição da distância')

