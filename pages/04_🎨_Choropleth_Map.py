import streamlit as st
import mapclassify
import matplotlib.pyplot as plt
from palettable import colorbrewer
from utils import local_css
from data_munging import load_data


combined_geo_incidents_df, regions_incidents = load_data()

sequential = colorbrewer.COLOR_MAPS['Sequential']
diverging = colorbrewer.COLOR_MAPS['Diverging']
qualitative = colorbrewer.COLOR_MAPS['Qualitative']

k_classifiers = {
    'quantiles': mapclassify.Quantiles,
    'equal_interval': mapclassify.EqualInterval,
    'fisher_jenks': mapclassify.FisherJenks,
    'jenks_caspall': mapclassify.JenksCaspall,
    'jenks_caspall_forced': mapclassify.JenksCaspallForced,
    'maximum_breaks': mapclassify.MaximumBreaks,
    'natural_breaks': mapclassify.NaturalBreaks
}


def replace_legend_items(legend, mapping):
    for txt in legend.texts:
        for k, v in mapping.items():
            if txt.get_text() == str(k):
                txt.set_text(v)


def map(method, k, cmap):
    classifier = k_classifiers[method](regions_incidents.n_events, k=k)
    mapping = dict([(i, s)
                   for i, s in enumerate(classifier.get_legend_classes())])

    f, ax = plt.subplots(1, figsize=(16, 9))
    regions_incidents.assign(cl=classifier.yb).plot(column='cl', categorical=True,
                                                    k=k, cmap=cmap, linewidth=0.1, ax=ax,
                                                    edgecolor='grey', legend=True,
                                                    legend_kwds={'loc': 'lower right'})
    ax.set_axis_off()
    ax.set_title('Number of incidents')
    replace_legend_items(ax.get_legend(), mapping)

    st.pyplot(f)


def app():

    local_css("style.css")

    st.title('Choropleth Map')

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

    row1_1, row1_2 = st.columns((3, 1))

    with row1_2:
        method_val = st.selectbox(
            "Select the data classification method", options=list(k_classifiers.keys()))

        data_type = st.radio(
            "Select the type of color palettes", ('Sequential', 'Diverging', 'Qualitative'))

        bindings = {'Sequential': range(3, 9+1),
                    'Diverging': range(3, 11+1),
                    'Qualitative': range(3, 12+1)}

        cmap_bindings = {'Sequential': list(sequential.keys()),
                         'Diverging': list(diverging.keys()),
                         'Qualitative': list(qualitative.keys())}

        class_val = st.selectbox(
            "Select the number of groups (bins)", options=bindings[data_type], index=2)

        cmap_val = st.selectbox(
            "Select the colormap", options=cmap_bindings[data_type])

    with row1_1:
        map(method=method_val, k=class_val, cmap=cmap_val)


app()
