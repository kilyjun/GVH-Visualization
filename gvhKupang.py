import streamlit as st
import pandas as pd
import datetime
import folium
from folium.plugins import MarkerCluster
from folium.plugins import MeasureControl
from folium.plugins import Draw
from branca.element import Template, MacroElement
from streamlit_folium import st_folium

st.set_page_config(
    page_title="GVH Indonesia Geolocation Database",
    page_icon="🏔",
    layout="wide",
)

# read csv as dataframe
df = pd.read_csv('kupangGeolocation221120.csv')

totalcount = df["Name of Location"].count()

st.title("GVH Indonesia Dashboard")

# creating a single-element container
placeholder = st.empty()

# setup dates
previous_date = datetime.datetime.strptime("06-06-2022", '%m-%d-%Y')
today = datetime.datetime.today()

# compute difference
ndays = (today - previous_date).days

for seconds in range(200):

    with placeholder.container():

        # create two columns
        kpi1, kpi2 = st.columns(2)

        # fill in those two columns with respective metrics or KPIs
        kpi1.metric(
            label="# of Locations",
            value= totalcount,
        )

        kpi2.metric(
            label = "# of Days Since First Exploration",
            value = ndays,
        )
