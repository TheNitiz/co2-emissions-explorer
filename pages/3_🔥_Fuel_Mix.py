import streamlit as st
import plotly.express as px
import pandas as pd
from utils.queries import get_country_list, get_fuel_mix

st.set_page_config(page_title="Fuel Mix", page_icon="🔥", layout="wide")

st.title("🔥 Fuel Mix Over Time")
st.caption("See how a country's emissions are split across fuel sources, year by year.")

countries_df = get_country_list()
all_countries = countries_df["Country"].tolist()

default_index = all_countries.index("India") if "India" in all_countries else 0

selected_country = st.selectbox("Select a country", options=all_countries, index=default_index)

df = get_fuel_mix(selected_country)

fuel_cols = ["Coal", "Oil", "Gas", "Cement", "Flaring", "Other"]
df_long = df.melt(id_vars="Year", value_vars=fuel_cols, var_name="Fuel", value_name="Emissions")
df_long = df_long.dropna(subset=["Emissions"])

if df_long.empty:
    st.warning(f"No fuel-type breakdown data available for {selected_country}.")
    st.stop()

fig = px.area(
    df_long,
    x="Year",
    y="Emissions",
    color="Fuel",
    labels={"Emissions": "Emissions (Mt CO2)"},
)
fig.update_layout(
    hovermode="x unified",
    legend_title_text="Fuel Source",
    margin=dict(t=20),
    height=550,
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader(f"{selected_country}: Latest Year Breakdown")
latest_row = df.dropna(subset=fuel_cols, how="all").sort_values("Year").iloc[-1]
latest_year = int(latest_row["Year"])

pie_data = latest_row[fuel_cols].dropna()

col1, col2 = st.columns([1, 1])
with col1:
    fig_pie = px.pie(
        values=pie_data.values,
        names=pie_data.index,
        title=f"Fuel Mix in {latest_year}",
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.dataframe(
        pie_data.rename("Emissions (Mt CO2)").to_frame(),
        use_container_width=True,
    )