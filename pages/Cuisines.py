import pandas as pd
import plotly.express as px
from Home import clean_code
import streamlit as st
from PIL import Image

st.set_page_config(page_title = 'Cuisines', page_icon = '🍴',layout="wide")

df = pd.read_csv('dataset/zomato.csv')
df = clean_code( df )


#============================================
# SIDEBAR 
#============================================

# Icon
image_path = 'images/zomato.jpg'
image = Image.open( image_path )
st.sidebar.image( image )

# Page description
st.sidebar.write('Here you can find information related types of cuisines in dataset')

# Sidebar widgets for filtering
selected_cuisines = st.sidebar.multiselect('Select cuisines', df['cuisines'].unique(),default = df['cuisines'].value_counts().nlargest(5).index.tolist(), help = 'All options are shown if none is selected')
selected_countries = st.sidebar.multiselect('Select countries', df['country'].unique(),default = df['country'].value_counts().nlargest(5).index.tolist(), help = 'All options are shown if none is selected')
selected_price_tyes = st.sidebar.multiselect('Select price tyeps', df['price_tye'].unique(), default = df['price_tye'].unique())

if not selected_cuisines:
    selected_cuisines = df['cuisines'].unique()
if not selected_countries:
    selected_countries = df['country'].unique()
if not selected_price_tyes:
    selected_price_tyes = df['price_tye'].unique()


# Filter the dataframe based on selected filters
filtered_data = df[ df['cuisines'].isin(selected_cuisines) & 
                    df['country'].isin(selected_countries) &
                    df['price_tye'].isin(selected_price_tyes) ]

#============================================
# DashBoard
#============================================

with st.container():
    col1, col2 = st.columns(2)
    
    with col1: #BAR CHART - Number of Votes per Cuisine 
        df_grouped = (filtered_data[['cuisines','votes']].groupby('cuisines')
                                                         .sum()
                                                         .reset_index()
                                                         .sort_values(by = 'votes', ascending = False) )
                    
        
        fig = px.bar(df_grouped, x = 'cuisines', y = 'votes',
                                 color_discrete_sequence = ['#ff4b4b']*len(df_grouped),
                                 text_auto = True)  
        
        fig.update_layout(xaxis_title = "",
                          yaxis_title = "",
                          title = "Number of Votes per Cuisine",
                          showlegend = False)
        
        st.plotly_chart(fig)

    with col2: #BAR CHART - Rating per Cuisine
        df_grouped = (  filtered_data[['cuisines','aggregate_rating']].groupby('cuisines')
                                                                      .mean()
                                                                      .reset_index()
                                                                      .sort_values(by = 'aggregate_rating',ascending = False) )
                        
        fig = px.bar(df_grouped , x = 'cuisines', y = 'aggregate_rating',
                                  color_discrete_sequence = ['#ff4b4b']*len(df_grouped) ,
                                  text_auto = True)  
        
        fig.update_layout(xaxis_title = "",
                          yaxis_title = "",
                          title = "Rating per Cuisine",
                          showlegend = False)
        
        st.plotly_chart(fig)

with st.container():
    col1, col2 = st.columns(2)

    with col1: #SCATTERPLOt - Relationship between Online Delivery, Table Booking and Restaurant Popularity
        df_grouped = (df[['has_online_delivery','has_table_booking','votes']].groupby(['has_table_booking','has_online_delivery']).agg({'votes': ['mean', 'count']})
                                                                             .reset_index())
        
        df_grouped.columns = ['has_table_booking', 'has_online_delivery', 'mean_votes', 'count_votes']

        fig = px.scatter(df_grouped, x = 'has_table_booking', y = 'has_online_delivery',
                                     color = 'count_votes', size = 'mean_votes',
                                     labels = {'mean_votes': 'Mean Votes', 'count_votes': 'Count of Restaurants'},
                                     color_continuous_scale = ['#F8B7B7', '#E31A1C'],
                                     hover_data = ['count_votes', 'mean_votes'],
                                     size_max = 50, opacity = 1)
     
        fig.update_layout(title = 'Relationship between Online Delivery, Table Booking and Restaurant Popularity',
                          xaxis_title ='Has Online Delivery',
                          yaxis_title ='Has Table booking')
        
        st.plotly_chart(fig)

    with col2: #BAR CHART - Mean Cost by Table Booking and Online Delivery
        df_grouped = ( df[['has_online_delivery','has_table_booking','average_cost_USD']].groupby(['has_table_booking','has_online_delivery'])
                                                                                         .mean()
                                                                                         .reset_index() )

        fig = px.bar(df_grouped, x = "has_online_delivery",
                                 y = "average_cost_USD",
                                 color = "has_table_booking",
                                 barmode = "group",
                                 labels = {"has_table_booking": "Table Booking", "average_cost_USD": "Average Cost for two (USD)"},
                                 color_discrete_sequence = ["#81beff", "#ff4b4b"], 
                                 category_orders = {"has_table_booking": ["Yes", "No"], "has_online_delivery": ["Yes", "No"]},
                                 text_auto = True)
        
        fig.update_layout(title = "Mean Cost by Table Booking and Online Delivery",
                          xaxis_title = "Online Delivery",
                          yaxis_title = "Average Cost (USD)",
                          legend = dict( yanchor = "top",  y = 0.97,
                                         xanchor = "right", x = 0.3) )
        
        st.plotly_chart(fig)
