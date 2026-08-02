import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.queries import get_global_yearly_totals, get_summary_stats, get_top_emitters, get_global_fuel_totals
from utils.sidebar_decor import add_sidebar_decoration
add_sidebar_decoration()

st.set_page_config(
    page_title="Global CO2 Emissions Explorer",
    page_icon="🌍",
    layout="wide",
)



hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding-top: 2rem;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ---- Hero section ----
st.markdown("""
    <div style="text-align: center; padding: 1rem 0 2rem 0;">
        <h1 style="font-size: 3rem; font-weight: 800; margin-bottom: 0.3rem;
                   background: linear-gradient(90deg, #E63946, #F4A261);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🌍 Global CO2 Emissions Explorer
        </h1>
        <p style="font-size: 1.15rem; color: #A0A0A0; max-width: 650px; margin: 0 auto;">
            Explore 270+ years of carbon emissions data across 190+ countries —
            trace how the world's energy story has unfolded, one year at a time.
        </p>
    </div>
""", unsafe_allow_html=True)

with st.expander("ℹ️ What do these numbers mean?"):
    st.markdown("""
    - **Mt CO2** = *Megatonnes of CO2* — one megatonne equals **1 million metric tons**.
      For scale, that's roughly the weight of 3 million cars.
    - **Total** = combined emissions from all sources (coal, oil, gas, cement production, and gas flaring) for a country in a given year.
    - **Per Capita** = emissions divided by population — this shows emissions *per person*, letting you fairly compare a small country to a huge one like China or India.
    """)


# ---- KPI row ----
stats = get_summary_stats().iloc[0]
latest_year = int(stats["LatestYear"])
total_latest = stats["TotalLatest"]
total_previous = stats["TotalPrevious"]
top_country = stats["TopEmitterLatest"]
pct_change = ((total_latest - total_previous) / total_previous) * 100 if total_previous else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(f"Global Emissions ({latest_year})", f"{total_latest:,.0f} Mt", f"{pct_change:+.1f}% vs {latest_year-1}")
with col2:
    st.metric(f"Top Emitter ({latest_year})", top_country)
with col3:
    st.metric("Years of Data", f"{2021 - 1750}+")
with col4:
    st.metric("Countries Tracked", "190+")

st.divider()

# ---- Global trend line, styled ----
st.subheader("📈 Global Emissions Over Time")
df_trend = get_global_yearly_totals()

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df_trend["Year"], y=df_trend["GlobalTotal"],
    mode="lines",
    line=dict(color="#E63946", width=2.5, shape="spline"),
    fill="tozeroy",
    fillcolor="rgba(230, 57, 70, 0.15)",
    hovertemplate="<b>%{x}</b><br>%{y:,.0f} Mt CO2<extra></extra>",
))
fig.update_layout(
    height=420,
    hovermode="x unified",
    margin=dict(t=20, l=0, r=0, b=0),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#FAFAFA"),
    xaxis=dict(showgrid=False, title=None),
    yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)", title="Total Emissions (Mt CO2)"),
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---- Top emitters ----
st.subheader(f"🏆 Top 10 Emitters ({latest_year})")
df_top = get_top_emitters(latest_year).sort_values("Total")

fig2 = go.Figure(go.Bar(
    x=df_top["Total"], y=df_top["Country"],
    orientation="h",
    marker=dict(
        color=df_top["Total"],
        colorscale=[[0, "#457B9D"], [1, "#E63946"]],
    ),
    text=df_top["Total"].apply(lambda v: f"{v:,.0f}"),
    textposition="outside",
    hovertemplate="<b>%{y}</b><br>%{x:,.0f} Mt CO2<extra></extra>",
))
fig2.update_layout(
    height=450,
    margin=dict(t=20, l=0, r=40, b=0),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#FAFAFA"),
    xaxis=dict(showgrid=False, title=None),
    yaxis=dict(title=None),
)
st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.divider()

st.subheader("🔥 Which Fuel Has Driven Global Emissions?")
st.caption("Global emissions by fuel source, summed across every country, year by year.")

FUEL_COLORS = {
    "Coal": "#E63946",
    "Oil": "#F4A261",
    "Gas": "#2A9D8F",
    "Cement": "#8D99AE",
    "Flaring": "#E9C46A",
    "Other": "#6D6875",
}

df_fuel = get_global_fuel_totals()
fuel_cols = ["Coal", "Oil", "Gas", "Cement", "Flaring", "Other"]

fig3 = go.Figure()
for fuel in fuel_cols:
    fig3.add_trace(go.Scatter(
        x=df_fuel["Year"],
        y=df_fuel[fuel],
        name=fuel,
        mode="lines",
        stackgroup="one",
        line=dict(width=0.5, color=FUEL_COLORS[fuel]),
        fillcolor=FUEL_COLORS[fuel],
        hovertemplate=f"<b>{fuel}</b><br>%{{x}}: %{{y:,.0f}} Mt CO2<extra></extra>",
    ))

fig3.update_layout(
    height=460,
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, title=None),
    margin=dict(t=30, l=0, r=0, b=0),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#FAFAFA"),
    xaxis=dict(showgrid=False, title=None),
    yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)", title="Emissions (Mt CO2)"),
)

st.plotly_chart(fig3, use_container_width=True)

latest_fuel_row = df_fuel.iloc[-1]
top_fuel = latest_fuel_row[fuel_cols].idxmax()
top_fuel_pct = (latest_fuel_row[top_fuel] / latest_fuel_row[fuel_cols].sum()) * 100
st.info(f"**Coal remains the single largest contributor** to global emissions" if top_fuel == "Coal"
        else f"**{top_fuel} is currently the largest contributor** to global emissions",
        icon="🔥")

# ---- Navigation cards ----
st.subheader("🧭 Explore Further")

nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)

with nav_col1:
    st.page_link("pages/1_🗺️_Global_Map.py", label="Global Map", icon="🗺️")
    st.caption("Watch emissions evolve across the world, year by year.")

with nav_col2:
    st.page_link("pages/2_📈_Compare_Countries.py", label="Compare Countries", icon="📈")
    st.caption("Put any countries side by side across any metric.")

with nav_col3:
    st.page_link("pages/3_🔥_Fuel_Mix.py", label="Fuel Mix", icon="🔥")
    st.caption("See how a country's energy sources have shifted.")

with nav_col4:
    st.page_link("pages/4_🏆_Leaderboard.py", label="Leaderboard", icon="🏆")
    st.caption("Rank top emitters and fastest decliners.")