import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("Police.csv")
col1, col2 = st.columns([1, 5])

########################Cambio 1: Background Color
col1.markdown(
    "<style>"
    "body { background-color: #e6f7ff; }"
    "</style>",
    unsafe_allow_html=True
)

########################Cambio 2: Imagen del San Francisco Police Department 
col1.image("sfpd.jpg", width=100)
col2.title("Police Incident Reports from 2018 to 2020 in San Francisco")


# Convert 'Incident Date' to datetime format
df['Incident Date'] = pd.to_datetime(df['Incident Date'])

#Pestañas para filtrar datos
st.sidebar.header("Filter Data")
police_district_input = st.sidebar.multiselect(
    'Police District',
    df.groupby('Police District').count().reset_index()['Police District'].tolist()
)
if len(police_district_input) > 0:
    df = df[df['Police District'].isin(police_district_input)]

#Neighborhood
neighborhood_input = st.sidebar.multiselect(
    'Neighborhood',
    df.groupby('Analysis Neighborhood').count().reset_index()['Analysis Neighborhood'].tolist()
)
if len(neighborhood_input) > 0:
    df = df[df['Analysis Neighborhood'].isin(neighborhood_input)]

#Incident Category
incident_input = st.sidebar.multiselect(
    'Incident Category',
    df.groupby('Incident Category').count().reset_index()['Incident Category'].tolist()
)
if len(incident_input) > 0:
    df = df[df['Incident Category'].isin(incident_input)]

#Filtros aplicados 
if len(police_district_input) > 0 or len(neighborhood_input) > 0 or len(incident_input) > 0:
    st.sidebar.markdown("**Applied Filters:**")
    if len(police_district_input) > 0:
        st.sidebar.markdown(f"- **Police District:** {', '.join(police_district_input)}")
    if len(neighborhood_input) > 0:
        st.sidebar.markdown(f"- **Neighborhood:** {', '.join(neighborhood_input)}")
    if len(incident_input) > 0:
        st.sidebar.markdown(f"- **Incident Category:** {', '.join(incident_input)}")

######################## Cambio 3
st.markdown(
    "Explore incident reports in San Francisco from 2018 to 2020, including details such as date, day of the week, "
    "police districts, neighborhoods, incident category, subcategory, location, and resolution."
)
st.markdown('Crime locations in San Francisco')
fig_map = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", color="Incident Category",
                            mapbox_style="stamen-terrain", zoom=10, hover_name="Incident Description")
st.plotly_chart(fig_map)

####################### Cambio 4
fig_bar_day = px.bar(df['Incident Day of Week'].value_counts(), x=df['Incident Day of Week'].value_counts().index,
                     y=df['Incident Day of Week'].value_counts().values, color_continuous_scale='Viridis',
                     labels={'y': 'Count', 'x': 'Day of the Week'}, title='Crimes per Day of the Week')
st.plotly_chart(fig_bar_day)

####################### Cambio 5
st.markdown('Crimes occurred per date')
fig_bar_date = px.bar(df['Incident Date'].value_counts(), x=df['Incident Date'].value_counts().index,
                      y=df['Incident Date'].value_counts().values,
                      labels={'y': 'Count', 'x': 'Date'}, title='Crimes per Date',
                      color=df['Incident Date'].value_counts().index, color_continuous_scale='Viridis')
st.plotly_chart(fig_bar_date)

####################### Cambio 6
fig_bar_category = px.bar(df['Incident Category'].value_counts(), x=df['Incident Category'].value_counts().index,
                          y=df['Incident Category'].value_counts().values, color_continuous_scale='Viridis',
                          labels={'y': 'Count', 'x': 'Incident Category'}, title='Crimes by Category')
st.plotly_chart(fig_bar_category)