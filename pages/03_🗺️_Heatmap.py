import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import HeatMap
from utils import local_css
from data_munging import load_data, get_min_max_date, get_dates_list, filter_by_date


def app():

    st.set_page_config(
        page_title="Heatmap - Geospatial Data Analysis of Civilian Harm in Ukraine",
        page_icon="🗺️",
        initial_sidebar_state="expanded",
        layout="wide"
    )

    local_css("style.css")

    st.title('Heatmap')

    with st.sidebar:
        st.title("About")
        st.info(
            """
                This project aims to extract statistical insights and produce a meaningful cartographic visualization of civilian harm in Ukraine.
        
                ---
                data - [Bellingcat](https://www.bellingcat.com/)
        
                author - [Oleksandr Pancheliuga](https://pancheliuga.com/) ©️ 2022 
                """
        )

    combined_geo_incidents_df, regions_incidents = load_data()

    min_date, max_date = get_min_max_date(combined_geo_incidents_df)

    dates_list = get_dates_list(combined_geo_incidents_df)

    start_date, end_date = st.select_slider(
        'Select the date range', dates_list, value=[min_date, max_date])

    filtered_by_date = filter_by_date(
        combined_geo_incidents_df, start_date, end_date)

    m = folium.Map(location=[49.107892273527504, 31.444630060047018],
                   tiles='stamentoner', zoom_start=6, control_scale=True)

    heat_data = list(zip(
        filtered_by_date["latitude"], filtered_by_date["longitude"]))

    HeatMap(heat_data).add_to(m)

    st_folium(m, width=1100)


app()
