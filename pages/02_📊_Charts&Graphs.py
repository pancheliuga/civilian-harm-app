import streamlit as st
import plotly.express
from utils import local_css
from data_munging import load_data, get_min_max_date, get_dates_list, filter_by_date, group_by_date, group_by_type, group_by_region

chart_types = {
    'line': plotly.express.line,
    'bar': plotly.express.bar
}


def chart(data, type):
    fig = chart_types[type](data, x='date', y='n_events',
                            title='Number of incidents per day', labels={'n_events': 'Number of incidents'})

    st.plotly_chart(fig, use_container_width=True)


def pie(params):
    fig = plotly.express.pie(params['data'], values=params['values'], names=params['names'], title=params['title'],
                             hover_data=params['hover_data'], labels=params['labels'])

    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(uniformtext_minsize=12,
                      uniformtext_mode='hide', width=800, height=600)

    st.plotly_chart(fig, use_container_width=True)


def app():
    st.set_page_config(
        page_title="Charts&Graphs - Spatial Data Analisis of Civilian Harm in Ukraine",
        page_icon="📊",
        initial_sidebar_state="expanded",
        layout="wide"
    )

    local_css("style.css")

    st.title('Charts & Graphs')

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

    row2_1, row2_2 = st.columns((3.5, .5))

    filtered_by_date = filter_by_date(
        combined_geo_incidents_df, start_date, end_date)

    incidents_by_day = group_by_date(filtered_by_date)

    with row2_2:
        chart_type = st.radio("Select the type of chart", ('line', 'bar'))

    with row2_1:
        chart(incidents_by_day, type=chart_type)

    row3_1, row3_2 = st.columns(2)

    incidents_by_type = group_by_type(filtered_by_date)

    incidents_by_region = group_by_region(filtered_by_date)

    incidents_by_type_params = {
        'data': incidents_by_type,
        'values': 'n_events',
        'names': 'area_type',
        'title': 'Civilian harm by type of affected area',
        'hover_data': ['n_events'],
        'labels': {'n_events': 'Number of incidents'}
    }

    incidents_by_region_params = {
        'data': incidents_by_region,
        'values': 'n_events',
        'names': 'ADM1_EN',
        'title': 'Civilian harm by region',
        'hover_data': ['n_events'],
        'labels': {'n_events': 'Number of incidents', 'ADM1_EN': 'Region'}
    }

    with row3_1:
        pie(incidents_by_type_params)

    with row3_2:
        pie(incidents_by_region_params)


app()
