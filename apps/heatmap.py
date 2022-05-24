import streamlit as st
import pandas as pd
import json
from streamlit_folium import st_folium
import folium
from folium.plugins import HeatMap

# Load data


@st.experimental_singleton
def load_data():
    fp = 'data/ukr-civharm-2022-05-20.json'
    with open(fp, 'r') as file:
        content = json.loads(file.read())
    data = pd.json_normalize(content, record_path='filters', meta=[
                             'id', 'date', 'latitude', 'longitude', 'location', 'description'])
    data = data[data['key'] == 'Type of area affected']
    data = data.rename(columns={'value': 'type of area affected'})
    data = data[['id', 'date', 'latitude', 'longitude', 'location',
                 'type of area affected', 'description']].set_index('id')
    return data


def app():

    data = load_data()

    locations = list(zip(data["latitude"], data["longitude"]))

    st.title('Heatmap')

    # Create a Map instance
    m = folium.Map(location=[49.107892273527504, 31.444630060047018],
                   tiles='stamentoner', zoom_start=6, control_scale=True)

    # Add heatmap to map instance
    # Available parameters: HeatMap(data, name=None, min_opacity=0.5, max_zoom=18, max_val=1.0, radius=25, blur=15, gradient=None, overlay=True, control=True, show=True)
    HeatMap(locations).add_to(m)

    # Show map
    st_folium(m, width=1000, height=600)
