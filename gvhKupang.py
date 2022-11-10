import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import json
import requests

APP_TITLE = "GVH Indonesia"
APP_SUB_TITLE = "Kupang"

def display_map():
    map = folium.Map(location=[-10.21, 123.66], zoom_start=10, scrollWheelZoom=True)

    tooltip = "Click for more info"

    # ADD MARKERS
    df = pd.read_csv('with info and category.csv')
    for index, row in df.iterrows():
        
        iframe = folium.IFrame('<h4><b>' + str(row['Name of Location']) + '</h4></b>' + row['Date First Explored'] + '<br>' + str(row['Projects Done']))

        if row['General Type of Project'] == 'Necessities':
            folium.Marker([row['Latitude'], row['Longitude']], popup=folium.Popup(iframe, min_width=250, max_width=250), tooltip=tooltip, icon=folium.Icon(color='blue')).add_to(map)
        elif row['General Type of Project'] == 'Sustainability':
            folium.Marker([row['Latitude'], row['Longitude']], popup=folium.Popup(iframe, min_width=250, max_width=250), tooltip=tooltip, icon=folium.Icon(color='green')).add_to(map)
        elif row['General Type of Project'] == 'Education':
            folium.Marker([row['Latitude'], row['Longitude']], popup=folium.Popup(iframe, min_width=250, max_width=250), tooltip=tooltip, icon=folium.Icon(color='red')).add_to(map)
        elif row['General Type of Project'] == 'Miscellaneous':
            folium.Marker([row['Latitude'], row['Longitude']], popup=folium.Popup(iframe, min_width=250, max_width=250), tooltip=tooltip, icon=folium.Icon(color='pink')).add_to(map)
        else:
            folium.Marker([row['Latitude'], row['Longitude']], popup=folium.Popup(iframe, min_width=250, max_width=250), tooltip=tooltip, icon=folium.Icon(color='orange')).add_to(map)

    st_map = st_folium(map, width = 700, height= 450)

def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    # LOAD DATA
    df = pd.read_csv('with info and category.csv')
    date = 'Date First Explored'
    field_name = 'Name of Location'
    metric_title = f'# of Locations Explored'

    total = df[field_name].count()
    st.metric(metric_title, total)
    st.metric("# of Days since First Exploration", 157)

    # DISPLAY FILTERS AND MAP
    display_map()


if __name__ == "__main__":
    main()

 