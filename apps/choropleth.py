import streamlit as st
import pandas as pd
import json
import leafmap

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

    # data = load_data()
    data = leafmap.examples.datasets.countries_geojson
    m = leafmap.Map()
    m.add_data(
        data,
        column='POP_EST',
        scheme='EqualInterval',
        cmap='Blues',
        legend_title='Population',
    )
    m.to_streamlit()
