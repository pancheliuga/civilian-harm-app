import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import HeatMap

from data_munging import load_data, get_min_max_date, get_dates_list, filter_by_date


def app():

    st.title('Heatmap')

    combined_geo_incidents_df, regions_incidents = load_data()

    min_date, max_date = get_min_max_date(combined_geo_incidents_df)

    dates_list = get_dates_list(combined_geo_incidents_df)

    row1_1, row1_2 = st.columns((3, 1))

    with row1_1:
        start_date, end_date = st.select_slider(
            'Select the date range', dates_list, value=[min_date, max_date])

    row2_1, row2_2 = st.columns((3, 1))

    filtered_by_date = filter_by_date(
        combined_geo_incidents_df, start_date, end_date)

    with row2_1:

        m = folium.Map(location=[49.107892273527504, 31.444630060047018],
                       tiles='stamentoner', zoom_start=6, control_scale=True)

        heat_data = list(zip(
            filtered_by_date["latitude"], filtered_by_date["longitude"]))

        HeatMap(heat_data).add_to(m)

        st_folium(m, width=1000, height=600)
