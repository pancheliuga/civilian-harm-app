import streamlit as st
from multiapp import MultiApp
from apps import (
    home,
    heatmap,
    choropleth
)

st.set_page_config(layout="wide")


apps = MultiApp()

# Add all your application here

apps.add_app("Home", home.app)
apps.add_app("Heatmap", heatmap.app)
apps.add_app("Choropleths", choropleth.app)

# The main app
apps.run()
