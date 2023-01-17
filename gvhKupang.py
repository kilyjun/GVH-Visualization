import streamlit as st
import pandas as pd
import datetime
import folium
from folium.plugins import MarkerCluster
from folium.plugins import MeasureControl
from folium.plugins import Draw
from branca.element import Template, MacroElement
from streamlit_folium import st_folium
import plotly.express as px 

st.set_page_config(
    page_title="GVH Indonesia Geolocation Database",
    page_icon="🏔",
    layout="wide",
)

# read csv as dataframe
df = pd.read_csv('kupangGeolocation221120.csv')

totalcount = df["Name of Location"].count()

st.title("GVH Indonesia Dashboard")

# # creating a single-element container
placeholder = st.empty()

# setup dates
previous_date = datetime.datetime.strptime("06-06-2022", '%m-%d-%Y')
today = datetime.datetime.today()

# compute difference
ndays = (today - previous_date).days

with placeholder.container():

    # create two columns
    kpi1, kpi2 = st.columns(2)

    # fill in those two columns with respective metrics or KPIs
    kpi1.metric(label="Number of Locations", value= totalcount,
    )

    kpi2.metric(label = "Number of Days Since First Exploration", value = ndays,
    )

if st.checkbox("Filter by Project Category"):
    # top-level filters
    category_filter = st.selectbox("Select Project Category", pd.unique(df["General Type of Project"]))
    # dataframe filter
    df = df[df["General Type of Project"] == category_filter]

# create a map
def display_map():
    map = folium.Map(location=[-10.21, 123.66], zoom_start=10, scrollWheelZoom=False)

    # add measure control
    map.add_child(MeasureControl())

    # add draw control
    draw = Draw()

    draw.add_to(map)

    map.save('map.html')

    # add marker cluster
    marker_cluster = MarkerCluster().add_to(map)

    # add tooltip
    tooltip = "Click for more info"

    # HTML Code for Legend

    template = """
    {% macro html(this, kwargs) %}

    <!doctype html>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>jQuery UI Draggable - Default functionality</title>
    <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

    <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
    
    <script>
    $( function() {
        $( "#maplegend" ).draggable({
                        start: function (event, ui) {
                            $(this).css({
                                right: "auto",
                                top: "auto",
                                bottom: "auto"
                            });
                        }
                    });
    });

    </script>
    </head>
    <body>

    
    <div id='maplegend' class='maplegend' 
        style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
        border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
        
    <div class='legend-title'>Legend </div>
    <div class='legend-scale'>
    <ul class='legend-labels'>
        <li><span style='background:orange;opacity:0.7;'></span>Necessities</li>
        <li><span style='background:green;opacity:0.7;'></span>Sustainability</li>
        <li><span style='background:red;opacity:0.7;'></span>Education</li>
        <li><span style='background:pink;opacity:0.7;'></span>Miscellaneous</li>
        <li><span style='background:lightblue;opacity:0.7;'></span>No project yet</li>
        

    </ul>
    </div>
    </div>
    
    </body>
    </html>

    <style type='text/css'>
    .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
    .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
    .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
    .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 1px solid #999;
        }
    .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
    .maplegend a {
        color: #777;
        }
    </style>
    {% endmacro %}"""

    macro = MacroElement()
    macro._template = Template(template)

    map.get_root().add_child(macro)

    folium.plugins.Fullscreen().add_to(map)
    
    # ADD MARKERS
    if st.checkbox("Cluster Markers"):
        for index, row in df.iterrows():
            
            iframe = folium.IFrame('<h4><b>' + str(row['Name of Location']) + '</h4></b>' + row['Date First Explored'] + '<br>' + str(row['Projects Done']))

            if row['General Type of Project'] == 'Necessities':
                folium.Marker([row['Latitude'], row['Longitude']], popup=folium.Popup(iframe, min_width=250, max_width=250), tooltip=tooltip, icon=folium.Icon(color='orange')).add_to(marker_cluster)
            elif row['General Type of Project'] == 'Sustainability':
                folium.Marker([row['Latitude'], row['Longitude']], popup=folium.Popup(iframe, min_width=250, max_width=250), tooltip=tooltip, icon=folium.Icon(color='green')).add_to(marker_cluster)
            elif row['General Type of Project'] == 'Education':
                folium.Marker([row['Latitude'], row['Longitude']], popup=folium.Popup(iframe, min_width=250, max_width=250), tooltip=tooltip, icon=folium.Icon(color='red')).add_to(marker_cluster)
            elif row['General Type of Project'] == 'Miscellanous':
                folium.Marker([row['Latitude'], row['Longitude']], popup=folium.Popup(iframe, min_width=250, max_width=250), tooltip=tooltip, icon=folium.Icon(color='pink')).add_to(marker_cluster)
            else:
                folium.Marker([row['Latitude'], row['Longitude']], popup=folium.Popup(iframe, min_width=250, max_width=250), tooltip=tooltip, icon=folium.Icon(color='lightblue')).add_to(marker_cluster)

    else:
        for index, row in df.iterrows():
            
            iframe = folium.IFrame('<h4><b>' + str(row['Name of Location']) + '</h4></b>' + row['Date First Explored'] + '<br>' + str(row['Projects Done']))

            if row['General Type of Project'] == 'Necessities':
                folium.Marker([row['Latitude'], row['Longitude']], popup=folium.Popup(iframe, min_width=250, max_width=250), tooltip=tooltip, icon=folium.Icon(color='orange')).add_to(map)
            elif row['General Type of Project'] == 'Sustainability':
                folium.Marker([row['Latitude'], row['Longitude']], popup=folium.Popup(iframe, min_width=250, max_width=250), tooltip=tooltip, icon=folium.Icon(color='green')).add_to(map)
            elif row['General Type of Project'] == 'Education':
                folium.Marker([row['Latitude'], row['Longitude']], popup=folium.Popup(iframe, min_width=250, max_width=250), tooltip=tooltip, icon=folium.Icon(color='red')).add_to(map)
            elif row['General Type of Project'] == 'Miscellanous':
                folium.Marker([row['Latitude'], row['Longitude']], popup=folium.Popup(iframe, min_width=250, max_width=250), tooltip=tooltip, icon=folium.Icon(color='pink')).add_to(map)
            else:
                folium.Marker([row['Latitude'], row['Longitude']], popup=folium.Popup(iframe, min_width=250, max_width=250), tooltip=tooltip, icon=folium.Icon(color='lightblue')).add_to(map)            

    st_map = st_folium(map, width = 1130, height= 500)

def main():

    # DISPLAY FILTERS AND MAP
    display_map()
    
if __name__ == "__main__":
    main()

# create 2 columns for 2 histogram and pie chart
fig_col1, fig_col2 = st.columns(2)
with fig_col1:
    st.markdown("Count of Projects by Type")
    fig = px.histogram(data_frame=df, x="General Type of Project")
    st.write(fig)
            
with fig_col2:
    st.markdown("Percentage of Projects by Type")
    fig = px.pie(data_frame=df, names="General Type of Project", color="General Type of Project"
                 , color_discrete_map={'Necessities':'orange', 'Sustainability':'green', 'Education':'red', 'Miscellanous':'pink', 'Other':'lightcyan'})
    st.write(fig)  

# create checkbox
if st.checkbox("Show Detailed Data View"):
    # Detailed View
    st.markdown("### Detailed Data View")
    st.dataframe(df)

