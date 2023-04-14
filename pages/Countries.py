import pandas as pd
import plotly.express as px
from Home import clean_code
import streamlit as st
from PIL import Image

st.set_page_config(page_title = 'Countries', page_icon = '🗺️',layout="wide")

df = pd.read_csv('dataset/zomato.csv')
df = clean_code( df )

def cloropleth_map(df,variable,title):
    fig = px.choropleth(df,
                        locations=df.index,
                        locationmode='country names',
                        color=variable,
                        title=title,
                        color_continuous_scale='Viridis_r',
                        labels={variable:''})
        
    fig.update_layout(geo=dict(projection_type='equirectangular'))

    # Set the color bar orientation to horizontal
    fig.update_layout(coloraxis_colorbar=dict(orientation='h', xanchor='center', x=0.5, y=-0.1))

    return fig
#============================================
# SIDEBAR 
#============================================

# Icon
image_path = 'images/zomato.jpg'
image = Image.open( image_path )
st.sidebar.image( image)

# Page description
st.sidebar.write('Here you can find information related to the countries where the ')

# Sidebar widgets for filtering
continent_filter = st.sidebar.multiselect("Filter by continent", df['continent'].unique(), help = 'All options are shown if none is selected')
price_type_filter = st.sidebar.multiselect("Filter by price type", df['price_tye'].unique(), help = 'All options are shown if none is selected')
display_countries_filter = st.sidebar.slider('Select how many countries to display', 1, 15,10)

if not continent_filter:
    continent_filter = df['continent'].unique()
if not price_type_filter:
    price_type_filter = df['price_tye'].unique()


# Filter the dataframe based on selected filters
filtered_data = df[df['continent'].isin(continent_filter)]
if len(price_type_filter) > 0:
    filtered_data = filtered_data[filtered_data['price_tye'].isin(price_type_filter)]


#============================================
# DASHBOARD 
#============================================

# Dictionary of coloring continents
continent_colors = {
    'Asia'          : '#e1861b',
    'Europe'        : '#C4E538',
    'North America' : '#12CBC4',
    'South America' : '#FF5733',
    'Africa'        : '#FDA7DF',
    'Oceania'       : '#ED4C67'
}

# Dictionary for coloring price tye
price_tye_colors = {
    'cheap'     : '#00FF7F',
    'normal'    : '#FFD700',
    'expensive' : '#FF6384',
    'gourmet'   : '#00BFFF'
}

tab1, tab2 = st.tabs(["Maps", "Charts"])

with tab1:

    
    df1 = df.copy()
    df1['has_online_delivery'] = df1[ 'has_online_delivery'].replace({'No':0,'Yes':1})
    cols = ['country','average_cost_USD','votes','aggregate_rating','cuisines','restaurant_id','has_online_delivery']
    df_grouped = df1.pivot_table(index='country',
                                 values=['average_cost_USD', 'aggregate_rating', 'votes', 'cuisines', 'restaurant_id', 'has_online_delivery'],
                                 aggfunc={'average_cost_USD'     : 'mean',
                                          'aggregate_rating'     : 'mean',
                                          'votes'                : 'sum',
                                          'has_online_delivery'  : 'sum',
                                          'cuisines'             : 'nunique',
                                          'restaurant_id'        : 'count'})
    
    col1,col2,col3 = st.columns(3)
 
    with st.container():

        with col1:
            fig = cloropleth_map(df_grouped,'average_cost_USD','Mean of Average Cost')
            st.plotly_chart(fig,use_container_width = True)
           
            fig = cloropleth_map(df_grouped,'has_online_delivery','Has online delivery')
            st.plotly_chart(fig,use_container_width = True)

        with col2:
            fig = cloropleth_map(df_grouped,'aggregate_rating','Mean Restaurants Rating')
            st.plotly_chart(fig,use_container_width = True)
          
            fig = cloropleth_map(df_grouped,'cuisines','Count of unique cuisines')
            st.plotly_chart(fig,use_container_width = True)           

        with col3:
            fig = cloropleth_map(df_grouped,'votes','Sum of Votes')
            st.plotly_chart(fig,use_container_width = True)
       
            fig = cloropleth_map(df_grouped,'restaurant_id','Count of restaurants')
            st.plotly_chart(fig,use_container_width = True)


with tab2:
        
    with st.container():

        df_grouped = (filtered_data[['country', 'average_cost_USD', 'continent']]
                        .groupby(['country', 'continent']).agg({'average_cost_USD': ['mean', 'std']})
                        .reset_index())
        
        df_grouped.columns = ['country', 'continent', 'average_cost_USD_mean', 'average_cost_USD_std']
        df_grouped = df_grouped.sort_values(by = 'average_cost_USD_mean', ascending = False)
        df_grouped = df_grouped.nlargest(display_countries_filter,'average_cost_USD_mean')

        fig = px.bar( df_grouped,x = 'country',
                                y = 'average_cost_USD_mean',
                                error_y = 'average_cost_USD_std',
                                color ='continent',
                                color_discrete_map = continent_colors)
        
        fig.update_traces(error_y_color = '#FFFF00')
        
        fig.update_layout(xaxis_title = "",
                        yaxis_title = "",
                        title = "Average Cost for two ($)",
                        legend = dict(yanchor =  "top",  y = 0.99,
                                        xanchor = "right", x = 1) )
        
        st.plotly_chart(fig, use_container_width = True)


    with st.container():
        col1, col2 = st.columns(2)

        with col1: # BAR CHART - Number of cities per country

            df_grouped = ( df[['country','city', 'continent']]
                            .groupby(['country', 'continent'])
                            .nunique()
                            .reset_index()
                            .sort_values( by = 'city', ascending = False )
                            .nlargest(display_countries_filter,'city') )
            
            fig = px.bar(df_grouped, x = 'country',
                                    y = 'city',
                                    color ='continent',
                                    color_discrete_map = continent_colors,
                                    text_auto = '.2s')

            fig.update_layout(xaxis_title = "",
                            yaxis_title = "",
                            title = "Number of Cities per Country",
                            showlegend = False)
            
            st.plotly_chart(fig, use_container_width = True)
            
        with col2: #BAR CHART - Number of restaurant per country

            df_grouped = ( df[['country','restaurant_id', 'continent']]
                            .groupby(['country', 'continent'])
                            .nunique()
                            .reset_index()
                            .sort_values(by = 'restaurant_id',ascending = False)
                            .nlargest(display_countries_filter,'restaurant_id') )
            
            fig = px.bar(df_grouped, x = 'country', 
                                    y = 'restaurant_id',
                                    color ='continent',
                                    color_discrete_map = continent_colors,
                                    text_auto = '.2s')

            fig.update_layout(xaxis_title = "",
                            yaxis_title = "",
                            title = "Number of Restaurants per Country",
                            showlegend = False)
                            
            st.plotly_chart(fig, use_container_width = True)


    with st.container(): #GROUPED BAR CHART - Number of votes per country

        #Store list of countries with most votes according to Display countries filter
        top_n_paises = ( filtered_data[['country', 'price_tye']]
                            .groupby('country')
                            .count()
                            .nlargest(display_countries_filter, 'price_tye').index )
        
        # Filter Data with only the selected countries
        df_filtered = filtered_data[filtered_data['country'].isin(top_n_paises)]

        # Count Coutries per price tye by filtered data 
        df_grouped = ( df_filtered[['country', 'price_tye', 'restaurant_id', 'continent']]
                        .groupby(['country', 'price_tye', 'continent'])
                        .count()
                        .reset_index()
                        .sort_values('restaurant_id', ascending=False))

        fig = px.bar(df_grouped,x = 'country', 
                                y = 'restaurant_id', 
                                barmode = 'group', 
                                color = 'price_tye',
                                category_orders = {'price_tye': ['cheap', 'normal', 'expensive', 'gourmet']},
                                color_discrete_map = price_tye_colors )
        
        fig.update_layout( xaxis_title = "",
                        yaxis_title = "",
                        title = "Number of Votes per Country",
                        legend = dict(yanchor = "top",  y = 0.99,
                                        xanchor = "right", x = 1) )
        
        st.plotly_chart(fig, use_container_width = True)

