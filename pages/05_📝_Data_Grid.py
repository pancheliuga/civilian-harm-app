import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, DataReturnMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode
from data_munging import load_data
from utils import local_css, download_button


def app():
    st.set_page_config(
        page_title="Data Grid",
        page_icon="📝",
        initial_sidebar_state="expanded",
        layout="wide"
    )

    local_css("style.css")

    st.title('Data Grid')

    st.info(
        """
        This ag-Grid table provides an easy way for data manipulating (e.g. filtering, sorting, and more). 
        """
    )

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

    gb = GridOptionsBuilder.from_dataframe(combined_geo_incidents_df)
    gb.configure_default_column(
        enablePivot=True, enableValue=True, enableRowGroup=True)
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    gb.configure_side_bar()
    gridOptions = gb.build()

    response = AgGrid(
        combined_geo_incidents_df,
        gridOptions=gridOptions,
        enable_enterprise_modules=True,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        fit_columns_on_grid_load=False,
    )

    st.success(
        f"""
        💡 Tip! Hold the shift key when selecting rows to select multiple rows at once!
        """
    )

    df = pd.DataFrame(response["selected_rows"])

    row1_1, row1_2, row1_3 = st.columns([.5, .5, 3])

    with row1_1:

        CSVButton = download_button(
            df,
            "File.csv",
            "Download to CSV",
        )

    with row1_2:
        CSVButton = download_button(
            df,
            "File.csv",
            "Download to TXT",
        )


app()
