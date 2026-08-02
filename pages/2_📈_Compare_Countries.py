import streamlit as st
import plotly.express as px
from utils.queries import get_country_list, get_country_comparison
from utils.sidebar_decor import add_sidebar_decoration
add_sidebar_decoration()

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

st.divider()

st.subheader("Full Data Matrix")
st.caption("Every country, every year, for a chosen metric. Search or export below.")

matrix_metric = st.selectbox(
    "Metric for matrix",
    options=["Total", "Coal", "Oil", "Gas", "Cement", "Flaring", "Other", "PerCapita"],
    index=0,
    key="matrix_metric",
)

with st.expander("View full matrix (large table — click to expand)"):
    from utils.queries import get_country_year_matrix

    df_matrix_long = get_country_year_matrix(matrix_metric)
    df_matrix = df_matrix_long.pivot(index="Year", columns="Country", values="Value")

    country_filter = st.multiselect(
        "Filter to specific countries (optional)",
        options=df_matrix.columns.tolist(),
        default=[],
        key="matrix_country_filter",
    )

    display_df = df_matrix[country_filter] if country_filter else df_matrix

    st.dataframe(display_df, use_container_width=True, height=500)

    csv_data = display_df.to_csv().encode("utf-8")
    st.download_button(
        label="Download this matrix as CSV",
        data=csv_data,
        file_name=f"{matrix_metric.lower()}_by_country_year.csv",
        mime="text/csv",
    )