import streamlit as st
import plotly.express as px
from utils.queries import get_country_list, get_country_comparison

st.set_page_config(page_title="Compare Countries", page_icon="📈", layout="wide")

st.title("📈 Compare Countries")
st.caption("Select countries and a metric to compare emission trends over time.")

countries_df = get_country_list()
all_countries = countries_df["Country"].tolist()

default_selection = [c for c in ["United States", "China", "India"] if c in all_countries]

selected_countries = st.multiselect(
    "Select countries",
    options=all_countries,
    default=default_selection,
)

metric = st.selectbox(
    "Metric",
    options=["Total", "Coal", "Oil", "Gas", "Cement", "Flaring", "Other", "PerCapita"],
    index=0,
)

if not selected_countries:
    st.warning("Select at least one country to see the comparison.")
    st.stop()

df = get_country_comparison(selected_countries, metric)

fig = px.line(
    df,
    x="Year",
    y="Value",
    color="Country",
    labels={"Value": f"{metric} Emissions (Mt CO2)" if metric != "PerCapita" else "Per Capita Emissions"},
)
fig.update_layout(
    hovermode="x unified",
    legend_title_text="",
    margin=dict(t=20),
    height=550,
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Raw Data")
st.dataframe(df.pivot(index="Year", columns="Country", values="Value"), use_container_width=True)