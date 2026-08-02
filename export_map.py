import plotly.express as px
from utils.queries import get_map_data

df = get_map_data(min_year=1950)

fig = px.choropleth(
    df,
    locations="ISO3",
    color="Total",
    hover_name="Country",
    hover_data={"Total": ":,.1f", "ISO3": False},
    animation_frame="Year",
    color_continuous_scale="Inferno",
    range_color=(0, df["Total"].quantile(0.97)),
    projection="natural earth",
)

fig.update_geos(
    showcoastlines=True, coastlinecolor="#2C3E50",
    showland=True, landcolor="#1C1F26",
    showocean=True, oceancolor="#0E1117",
    showframe=False,
    bgcolor="rgba(0,0,0,0)",
)

fig.update_layout(
    height=600,
    margin=dict(l=0, r=0, t=10, b=0),
    paper_bgcolor="#0E1117",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#FAFAFA"),
)

fig.write_html("co2_map.html", include_plotlyjs="cdn", full_html=True)
print("Exported to co2_map.html")