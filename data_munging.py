import streamlit as st
import json
import pandas as pd
import geopandas as gpd
import numpy as np


@st.experimental_memo
def load_data():
    fp = 'data/ukr-civharm-2022-12-15.json'

    with open(fp, 'r') as file:
        data = json.loads(file.read())

    incidents_df = pd.json_normalize(data, record_path='filters', meta=[
                                     'id', 'date', 'latitude', 'longitude', 'location', 'description'])
    incidents_df = incidents_df[incidents_df['key'] == 'Type of area affected'].rename(
        columns={'value': 'area_type'}).reset_index()
    columns = [
        'id',
        'date',
        'latitude',
        'longitude',
        'location',
        'area_type',
        'description'
    ]
    incidents_df = incidents_df[columns]
    incidents_df[["latitude", "longitude"]] = incidents_df[[
        "latitude", "longitude"]].apply(pd.to_numeric)
    incidents_df['date'] = pd.to_datetime(incidents_df['date']).dt.date
    incidents_df = incidents_df.sort_values(by='date')
    geo_incidents_df = gpd.GeoDataFrame(incidents_df, geometry=gpd.points_from_xy(
        incidents_df['longitude'], incidents_df['latitude']), crs="EPSG:4326")
    geo_incidents_df.to_crs(epsg=3857, inplace=True)
    regions = gpd.read_file(
        'data/ukr-adm-sspe-20220131-zip-1/ukr_admbnda_adm1_sspe_20220114.shp')
    regions.to_crs(epsg=3857, inplace=True)
    combined_geo_incidents_df = gpd.sjoin(geo_incidents_df, regions[[
                                          'ADM1_EN', 'geometry']], predicate='within').drop(columns=['index_right'])

    incidents_by_region = combined_geo_incidents_df.groupby(
        'ADM1_EN').size().to_frame(name='n_events').reset_index()
    regions_incidents = pd.merge(
        regions[['ADM1_EN', 'geometry']], incidents_by_region, how='left', on='ADM1_EN')
    regions_incidents['n_events'] = regions_incidents['n_events'].fillna(0)

    return combined_geo_incidents_df, regions_incidents


def get_min_max_date(df):
    min_date = df['date'].min()
    max_date = df['date'].max()

    return min_date, max_date


def get_dates_list(df):
    return np.sort(df['date'].unique())


def filter_by_date(df, start_date, end_date):
    return df[(df['date'] >= start_date) & (df['date'] <= end_date)]


def group_by_date(df):
    return df.groupby('date').size().to_frame(name='n_events').reset_index()


def group_by_type(df):
    return df.groupby('area_type').size().to_frame(name='n_events').reset_index()


def group_by_region(df):
    return df.groupby('ADM1_EN').size().to_frame(name='n_events').reset_index()
