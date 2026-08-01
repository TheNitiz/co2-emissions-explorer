import streamlit as st
import plotly.express as px
from utils.queries import get_top_emitters, get_fastest_decliners
from utils.db import run_query

st.set_page_config(page_title="Leaderboard", page_icon="🏆", layout="wide")

st.title("🏆 Emissions Leaderboard")
st.caption("Who emits the most — and who's cutting the fastest.")

max_year = run_query("SELECT MAX(Year) AS y FROM emission WHERE Country <> 'Global'").iloc[0]["y"]
max_year = int(max_year)

tab1, tab2 = st.tabs(["Top Emitters", "Fastest Coal Decliners"])

with tab1:
    year = st.slider("Year", 1900, max_year, max_year, key="top_year")
    limit = st.slider("Show top N", 5, 25, 10, key="top_limit")

    df_top = get_top_emitters(year, limit)

    fig = px.bar(
        df_top.sort_values("Total"),
        x="Total",
        y="Country",
        orientation="h",
        text="Total",
        labels={"Total": "Total Emissions (Mt CO2)"},
    )
    fig.update_traces(marker_color="#457B9D", texttemplate="%{text:.0f}", textposition="outside")
    fig.update_layout(margin=dict(t=20), height=500)
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df_top.reset_index(drop=True), use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        start_year = st.number_input("Start year", min_value=1900, max_value=max_year - 1, value=2000)
    with col2:
        end_year = st.number_input("End year", min_value=start_year + 1, max_value=max_year, value=max_year)

    df_decline = get_fastest_decliners(int(start_year), int(end_year), limit=10)

    if df_decline.empty:
        st.warning("No countries with valid Coal data for this range.")
    else:
        fig2 = px.bar(
            df_decline.sort_values("PctChange", ascending=False),
            x="PctChange",
            y="Country",
            orientation="h",
            labels={"PctChange": "% Change in Coal Emissions"},
        )
        fig2.update_traces(marker_color="#2A9D8F")
        fig2.update_layout(margin=dict(t=20), height=450)
        st.plotly_chart(fig2, use_container_width=True)

        st.dataframe(df_decline.reset_index(drop=True), use_container_width=True)

        st.caption(f"Negative % = decline in coal emissions from {int(start_year)} to {int(end_year)}.")