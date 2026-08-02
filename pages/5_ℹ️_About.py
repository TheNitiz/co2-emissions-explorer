import streamlit as st
from utils.db import run_query
from utils.sidebar_decor import add_sidebar_decoration
add_sidebar_decoration()

st.set_page_config(page_title="About", page_icon="ℹ️", layout="wide")

st.title("ℹ️ About This Project")

st.markdown("""
### What this is
An interactive explorer for global CO2 emissions data, covering **270+ years** across
**190+ countries**, broken down by fuel source (coal, oil, gas, cement, flaring, and other).
""")

coverage = run_query(
    "SELECT MIN(Year) AS MinYear, MAX(Year) AS MaxYear, COUNT(DISTINCT Country) AS Countries "
    "FROM emission WHERE Country <> 'Global';"
).iloc[0]

col1, col2, col3 = st.columns(3)
col1.metric("Data From", int(coverage["MinYear"]))
col2.metric("Data To", int(coverage["MaxYear"]))
col3.metric("Countries Covered", int(coverage["Countries"]))

st.divider()

st.markdown("""
### Data source
This dataset is derived from the **Global Carbon Budget**, published by the
**Global Carbon Project** — the internationally recognized source for tracking
global and national CO2 emissions from fossil fuels, industry, and land-use change.

**Citation:**
Friedlingstein et al. (2025), *Global Carbon Budget 2025*, Earth System Science Data (ESSD).

**Acknowledgement:**
We acknowledge the Global Carbon Project, which is responsible for the Global Carbon
Budget, and thank the modelling groups for producing and making available their
model output.

Full dataset and documentation available at
[globalcarbonbudget.org](https://globalcarbonbudget.org).

*This is an independent, non-commercial portfolio project built for educational and
demonstration purposes. It is not affiliated with or endorsed by the Global Carbon
Project.*

### Methodology notes
- **Total** reflects combined emissions across all tracked sources (Coal, Oil, Gas,
  Cement, Flaring, Other), measured in **megatonnes of CO2 (Mt CO2)** — 1 megatonne
  = 1 million metric tons.
- **Per Capita** emissions are measured in **tonnes of CO2 per person per year**

### Tech stack
- **Database:** MySQL (hosted on Aiven)
- **Backend/Data layer:** Python, pandas, SQLAlchemy
- **Frontend:** Streamlit + Plotly
- **Deployment:** Streamlit Community Cloud

### Source code
The full pipeline — SQL schema, import scripts, and app code — is available on GitHub:

[github.com/TheNitiz/co2-emissions-explorer](https://github.com/TheNitiz/co2-emissions-explorer)
""")

st.info("Built as a portfolio project to demonstrate an end-to-end data pipeline: "
        "from raw CSV, to a cloud-hosted relational database, to an interactive analytics app.")