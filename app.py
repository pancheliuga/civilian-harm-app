import streamlit as st
from apps import (
    home,
    charts,
    heatmap,
    choropleth,
    aggrid
)


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def main():
    st.set_page_config(
        page_title="Spatial Data Analisis of Civilian Harm in Ukraine",
        page_icon="💣",
        initial_sidebar_state="expanded",
        layout="wide",
    )

    pages = {
        "home": home.app,
        "charts": charts.app,
        "heatmap": heatmap.app,
        "choropleth": choropleth.app,
        "aggrid": aggrid.app,
    }

    if "page" not in st.session_state:
        st.session_state.update(
            {
                # Default page
                "page": "home",
            }
        )

    local_css("style.css")

    with st.sidebar:
        if st.button("🏠 Home"):
            st.session_state.page = "home"
        if st.button("📊 Charts & Graphs"):
            st.session_state.page = "charts"
        if st.button("🗺️ Heatmap"):
            st.session_state.page = "heatmap"
        if st.button("🎨 Choropleth Map"):
            st.session_state.page = "choropleth"
        if st.button("📝 Data Grid"):
            st.session_state.page = "aggrid"
        st.markdown(
            """
            ---
            """
        )

        st.title("About")
        st.info(
            """
        This project aims to extract statistical insights and produce a meaningful cartographic visualization of civilian harm in Ukraine.
        
        ---

        data - [Bellingcat](https://www.bellingcat.com/)
        
        author - [Oleksandr Pancheliuga](https://pancheliuga.com/) ©️ 2022 
        """
        )

    pages[st.session_state.page]()


if __name__ == "__main__":
    main()
