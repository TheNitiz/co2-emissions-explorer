import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.queries import get_country_list, get_fuel_mix
from utils.sidebar_decor import add_sidebar_decoration
add_sidebar_decoration()

st.set_page_config(page_title="Fuel Mix", page_icon="🔥", layout="wide")

# Custom fuel color palette — warm, distinct, readable on dark background
FUEL_COLORS = {
    "Coal": "#E63946",
    "Oil": "#F4A261",
    "Gas": "#2A9D8F",
    "Cement": "#8D99AE",
    "Flaring": "#E9C46A",
    "Other": "#6D6875",
}

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

latest_row = df.dropna(subset=fuel_cols, how="all").sort_values("Year").iloc[-1]
latest_year = int(latest_row["Year"])
pie_data = latest_row[fuel_cols].dropna()
dominant_fuel = pie_data.idxmax()
dominant_pct = (pie_data.max() / pie_data.sum()) * 100

# ---- KPI row ----
col1, col2, col3 = st.columns(3)
col1.metric("Latest Year", latest_year)
col2.metric("Dominant Source", dominant_fuel, f"{dominant_pct:.0f}% of mix")
col3.metric("Fuel Types Tracked", len(pie_data))

st.divider()

# ---- Stacked, smoothed area chart ----
st.subheader(f"{selected_country}: Emissions by Fuel Source")

fig = go.Figure()
for fuel in fuel_cols:
    sub = df_long[df_long["Fuel"] == fuel]
    if sub.empty:
        continue
    fig.add_trace(go.Scatter(
        x=sub["Year"],
        y=sub["Emissions"],
        name=fuel,
        mode="lines",
        stackgroup="one",
        line=dict(width=0.5, color=FUEL_COLORS.get(fuel, "#999")),
        fillcolor=FUEL_COLORS.get(fuel, "#999"),
        hovertemplate=f"<b>{fuel}</b><br>%{{x}}: %{{y:,.1f}} Mt<extra></extra>",
    ))

fig.update_layout(
    height=520,
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, title=None),
    margin=dict(t=40, l=0, r=0, b=0),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#FAFAFA"),
    xaxis=dict(showgrid=False, title=None),
    yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)", title="Emissions (Mt CO2)"),
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---- Donut chart + breakdown table, side by side ----
col_left, col_right = st.columns([1.1, 1])

with col_left:
    st.subheader(f"Mix in {latest_year}")
    fig_donut = go.Figure(data=[go.Pie(
        labels=pie_data.index,
        values=pie_data.values,
        hole=0.55,
        marker=dict(colors=[FUEL_COLORS.get(f, "#999") for f in pie_data.index]),
        textinfo="label+percent",
        textfont=dict(color="#FAFAFA", size=13),
        hovertemplate="<b>%{label}</b><br>%{value:,.1f} Mt (%{percent})<extra></extra>",
    )])
    fig_donut.update_layout(
        height=400,
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=10, b=10, l=10, r=10),
        annotations=[dict(
        text=f"{pie_data.sum():,.0f}<br><span style='font-size:12px'>Mt CO2 Total</span>"
    )],)
    st.plotly_chart(fig_donut, use_container_width=True)

with col_right:
    st.subheader("Breakdown")
    for fuel in pie_data.sort_values(ascending=False).index:
        pct = (pie_data[fuel] / pie_data.sum()) * 100
        st.markdown(f"**{fuel}**")
        st.progress(pct / 100, text=f"{pie_data[fuel]:,.1f} Mt · {pct:.1f}%")