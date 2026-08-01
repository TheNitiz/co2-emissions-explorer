import streamlit as st
import plotly.express as px
from utils.queries import get_global_yearly_totals, get_summary_stats, get_top_emitters

st.set_page_config(
    page_title="Global CO2 Emissions Explorer",
    page_icon="🌍",
    layout="wide",
)

hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("🌍 Global CO2 Emissions Explorer")
st.caption("Exploring 270+ years of carbon emissions data, by country and fuel source.")

# ---- KPI row ----
stats = get_summary_stats().iloc[0]
latest_year = int(stats["LatestYear"])
total_latest = stats["TotalLatest"]
total_previous = stats["TotalPrevious"]
top_country = stats["TopEmitterLatest"]

pct_change = ((total_latest - total_previous) / total_previous) * 100 if total_previous else 0

col1, col2, col3 = st.columns(3)
col1.metric(f"Global Emissions ({latest_year})", f"{total_latest:,.0f} Mt", f"{pct_change:+.1f}% vs {latest_year-1}")
col2.metric(f"Top Emitter ({latest_year})", top_country)
col3.metric("Years of Data", f"1750 – {latest_year}")
st.divider()

# ---- Global trend line ----
st.subheader("Global Emissions Over Time")
df_trend = get_global_yearly_totals()

fig = px.line(
    df_trend,
    x="Year",
    y="GlobalTotal",
    labels={"GlobalTotal": "Total Emissions (Mt CO2)"},
)
fig.update_traces(line_color="#E63946", line_width=2)
fig.update_layout(hovermode="x unified", margin=dict(t=20))
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---- Top emitters this year ----
st.subheader(f"Top 10 Emitters ({latest_year})")
df_top = get_top_emitters(latest_year)

fig2 = px.bar(
    df_top.sort_values("Total"),
    x="Total",
    y="Country",
    orientation="h",
    labels={"Total": "Total Emissions (Mt CO2)"},
)
fig2.update_traces(marker_color="#457B9D")
fig2.update_layout(margin=dict(t=20))
st.plotly_chart(fig2, use_container_width=True)

st.info("Use the sidebar to explore the interactive map, compare countries, and dig into fuel-mix breakdowns.")