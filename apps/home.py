import streamlit as st


def app():

    st.title("Spatial Data Analisis of Civilian Harm in Ukraine")

    st.markdown(
        """
        #### *This project aims to extract statistical insights and produce a meaningful cartographic visualization of civilian harm in Ukraine.*
        """
    )

    st.info(
        "👈 Click on the left sidebar menu to navigate to the different analytical tools.")

    st.markdown(
        """
        *The data for this project based on incidents in Ukraine that have resulted in potential civilian harm. This data began collection by the OSINT group [Bellingcat](https://www.bellingcat.com/) on February 24, 2022, and intends to be a living document that will continue to be updated as long as the war persists. Therefore, this data is not an exhaustive list of civilian harm in Ukraine but rather a representation of all incidents that Bellingcat has collected and determined the exact locations.*
    """
    )

    row1_1, row1_2 = st.columns(2)
    with row1_1:
        st.image("img/heatmap.png")
        st.image("img/choropleth.png")

    with row1_2:
        st.image("img/griddata.gif")
        st.image("img/pie_chart.png")
