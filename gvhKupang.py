import streamlit as st
import datetime

# creating a single-element container
placeholder = st.empty()

# setup dates
previous_date = datetime.datetime.strptime("06-06-2022", '%m-%d-%Y')
today = datetime.datetime.today()

# compute difference
ndays = (today - previous_date).days
totalcount = 10

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
