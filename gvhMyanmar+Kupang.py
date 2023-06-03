import streamlit as st
import pandas as pd
import datetime
import folium
from folium.plugins import MarkerCluster
from folium.plugins import MeasureControl
from folium.plugins import Draw
from branca.element import Template, MacroElement
import plotly.express as px 
import streamlit.components.v1 as components

st.set_page_config(
    page_title="GVH Myanmar Dashboard",
    page_icon="🏔",
    layout="wide",
)

# read csv as dataframe
df = pd.read_csv('Myanmar+Kupang.csv')

# Drop rows with NaN values in 'Latitude' or 'Longitude'
df = df.dropna(subset=['Latitude', 'Longitude'])

totalcount = df["Name of Events"].count()

st.title("GVH Myanmar Dashboard")

# creating a single-element container
placeholder = st.empty()

# setup dates
previous_date = datetime.datetime.strptime("2020", '%Y')  # update the format according to the date in your CSV
today = datetime.datetime.today()

# compute difference
ndays = (today - previous_date).days

with placeholder.container():

    # create two columns
    kpi1, kpi2 = st.columns(2)

    # fill in those two columns with respective metrics or KPIs
    kpi1.metric(label="Number of Events", value= totalcount)

    kpi2.metric(label = "Number of Days Since First Event", value = ndays)

if st.checkbox("Filter by Project Category"):
    # top-level filters
    category_filter = st.selectbox("Select Project Category", pd.unique(df["General Type of Project"]))
    # dataframe filter
    df = df[df["General Type of Project"] == category_filter]

# create a map
def display_map():
    mean_lat = df['Latitude'].dropna().mean()
    mean_long = df['Longitude'].dropna().mean()

    map = folium.Map(location=[mean_lat, mean_long], zoom_start=5, scrollWheelZoom=True)

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
    </head>
    <body>
    <div id='maplegend' class='maplegend' 
        style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
         border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>

    <div class='legend-title'>Legend</div>
    <div class='legend-scale'>
      <ul class='legend-labels'>
        <li><span style='background:red;opacity:0.7;'></span>Necessities</li>
        <li><span style='background:green;opacity:0.7;'></span>Sustainability</li>
        <li><span style='background:blue;opacity:0.7;'></span>Education</li>
        <li><span style='background:orange;opacity:0.7'></span>Miscellaneous</li>
        <li><span style='background:pink;opacity:0.7'></span>Other</li>

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

    # assign marker colors
    for (index, row) in df.iterrows():
        if row["General Type of Project"] == "Necessities":
            marker_color = 'red'
        elif row["General Type of Project"] == "Sustainability":
            marker_color = 'green'
        elif row["General Type of Project"] == "Education":
            marker_color = 'blue'
        elif row["General Type of Project"] == "Miscellaneous":
            marker_color = 'orange'
        else:
            marker_color = 'pink'

        # create the popup content with a larger, scrollable box
        popup_content = f"<div style='max-height: 200px; overflow-y: scroll;'><strong>Name of Event:</strong> {row['Name of Events']}<br><br><strong>Update/General Description:</strong> {row['Update/ General Description']}<br><br><strong>Location:</strong> {row['Location']}</div>"

        # add marker
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(popup_content, max_width=400),
            tooltip=tooltip,
            icon=folium.Icon(color=marker_color)
        ).add_to(marker_cluster)

    # Add Legend
    macro = MacroElement()
    macro._template = Template(template)

    map.get_root().add_child(macro)

    map.save('map.html')  # Save it as html

    HtmlFile = open("map.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 

    return source_code  # return the HTML source code

# display the map
components.html(display_map(), width=1200, height=800)

# create 2 columns for 2 histogram and pie chart
fig_col1, fig_col2 = st.columns(2)
with fig_col1:
    st.markdown("Count of Projects by Type")
    fig = px.histogram(data_frame=df, x="General Type of Project")
    st.write(fig)
            
with fig_col2:
    st.markdown("Percentage of Projects by Type")
    fig = px.pie(data_frame=df, names="General Type of Project", color="General Type of Project",
                 color_discrete_map={'Necessities': 'orange', 'Sustainability': 'green', 'Education': 'blue', 'Miscellaneous': 'orange', 'Other': 'pink'})
    st.write(fig) 

# display the dataframe
st.dataframe(df)
