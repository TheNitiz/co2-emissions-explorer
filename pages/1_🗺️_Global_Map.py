import streamlit as st
import plotly.express as px
from utils.queries import get_map_data

st.set_page_config(page_title="Global Map", page_icon="🗺️", layout="wide")

st.title("🗺️ Global Emissions Map")
st.caption("Drag the slider or hit play to watch emissions evolve over time.")

metric = st.radio(
    "Metric",
    options=["Total", "PerCapita"],
    horizontal=True,
    format_func=lambda x: "Total Emissions" if x == "Total" else "Per Capita Emissions",
)

min_year = st.slider("Start from year", 1900, 2021, 1950)

df = get_map_data(min_year=min_year)

fig = px.choropleth(
    df,
    locations="ISO3",
    color=metric,
    hover_name="Country",
    animation_frame="Year",
    color_continuous_scale="OrRd",
    range_color=(0, df[metric].quantile(0.97)),  # clip outliers so the scale isn't washed out
    projection="natural earth",
)

fig.update_layout(
    height=650,
    margin=dict(l=0, r=0, t=20, b=0),
    coloraxis_colorbar=dict(title=metric),
)

st.plotly_chart(fig, use_container_width=True)

st.info("Note: darker red = higher emissions. Use the play button below the map to animate through years.")