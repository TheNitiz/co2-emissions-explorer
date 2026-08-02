import streamlit as st
import plotly.express as px
from utils.queries import get_map_data
from utils.sidebar_decor import add_sidebar_decoration
add_sidebar_decoration()


st.set_page_config(page_title="Global Map", page_icon="🗺️", layout="wide")

st.title("🗺️ Global Emissions Map")
st.caption("📏 Values shown in **Mt CO2** (megatonnes of CO2) for Total, or **tonnes per person** for Per Capita.")

col1, col2 = st.columns([1, 1])
with col1:
    metric = st.radio(
        "Metric",
        options=["Total", "PerCapita"],
        horizontal=True,
        format_func=lambda x: "Total Emissions" if x == "Total" else "Per Capita Emissions",
    )
with col2:
    color_scale = st.selectbox(
        "Color theme",
        options=["Inferno", "Plasma", "Turbo", "OrRd", "Viridis"],
        index=0,
    )

min_year = st.slider("Start from year", 1900, 2021, 1950)

df = get_map_data(min_year=min_year)

fig = px.choropleth(
    df,
    locations="ISO3",
    color=metric,
    hover_name="Country",
    hover_data={metric: ":,.1f", "ISO3": False},
    animation_frame="Year",
    color_continuous_scale=color_scale,
    range_color=(0, df[metric].quantile(0.97)),
    projection="natural earth",
)

fig.update_geos(
    showcoastlines=True, coastlinecolor="#2C3E50",
    showland=True, landcolor="#1C1F26",
    showocean=True, oceancolor="#0E1117",
    showlakes=False,
    showframe=False,
    bgcolor="rgba(0,0,0,0)",
)

fig.update_layout(
    height=680,
    margin=dict(l=0, r=0, t=10, b=0),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#FAFAFA", family="sans-serif"),
    coloraxis_colorbar=dict(
        title=dict(text=metric, font=dict(color="#FAFAFA")),
        tickfont=dict(color="#FAFAFA"),
        thickness=15,
        len=0.6,
    ),
)

# Slow the animation down slightly and smooth the transition
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 500
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 300

st.plotly_chart(fig, use_container_width=True)

st.info("Darker/brighter = higher emissions. Use the play button below the map to animate through years.")

# --- NEW: DYNAMIC EMBED LINK GENERATOR ---
with st.expander("🔌 Embed This Map on Your Website"):
    st.markdown("Want to show this dashboard on your portfolio or blog? Copy the HTML snippet below:")
    
    # Replace this string with your live deployed Streamlit URL
    LIVE_APP_URL = "https://streamlit.app"
    
    # Safe fallback parameter modification to bypass iframe redirect loops
    embed_url = f"{LIVE_APP_URL}/?embed=true&embed_options=disable_scrolling"
    
    # Generate the clean HTML code block
    iframe_snippet = f"""<iframe 
    src="{embed_url}" 
    width="100%" 
    height="600px" 
    style="border:none; border-radius:8px;" 
    allowfullscreen>
</iframe>"""

    # Displays a box with a "Copy code" button automatically built into Streamlit
    st.code(iframe_snippet, language="html")
