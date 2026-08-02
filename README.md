\# 🌍 Global CO2 Emissions Explorer



An interactive data explorer covering 270+ years of global CO2 emissions,

built end-to-end: cloud MySQL database → Python data pipeline → deployed

Streamlit + Plotly app.



\*\*\[🔗 Live App](https://your-app-name.streamlit.app)\*\*



!\[Landing page screenshot](assets/screenshot-home.png)



\## Features



\- 🗺️ \*\*Animated choropleth map\*\* — watch emissions evolve across 190+ countries, year by year

\- 📈 \*\*Country comparison\*\* — compare any countries across any metric (Total, Coal, Oil, Gas, Cement, Flaring, Per Capita)

\- 🔥 \*\*Fuel mix breakdown\*\* — see how a country's energy sources have shifted over time

\- 🏆 \*\*Leaderboard\*\* — top emitters by year, and fastest coal-decliners via a SQL self-join

\- 📊 \*\*Full data matrix\*\* — exportable country × year grid for any metric



\## Tech Stack



| Layer | Tool |

|---|---|

| Database | MySQL (hosted on Aiven) |

| Data pipeline | Python, pandas, SQLAlchemy |

| Frontend | Streamlit + Plotly |

| Deployment | Streamlit Community Cloud |



\## Data Source



Data from the \*\*Global Carbon Project's Global Carbon Budget\*\* (Friedlingstein et al., 2025, ESSD). See the in-app About page for full citation and fair-use details.



\## Architecture



\## Local Setup



```bash

git clone https://github.com/TheNitiz/co2-emissions-explorer.git

cd co2-emissions-explorer

python -m venv venv

source venv/Scripts/activate   # Windows Git Bash

pip install -r requirements.txt

```



Create a `.env` file with your own database credentials:



Run:



```bash

streamlit run Home.py

```



\## Database Schema



```sql

CREATE TABLE emission (

&#x20;   id            INT AUTO\_INCREMENT PRIMARY KEY,

&#x20;   Country       VARCHAR(100),

&#x20;   ISO3          CHAR(3),

&#x20;   Year          SMALLINT,

&#x20;   Total         DECIMAL(12,6),

&#x20;   Coal          DECIMAL(12,6),

&#x20;   Oil           DECIMAL(12,6),

&#x20;   Gas           DECIMAL(12,6),

&#x20;   Cement        DECIMAL(12,6),

&#x20;   Flaring       DECIMAL(12,6),

&#x20;   Other         DECIMAL(12,6),

&#x20;   PerCapita     DECIMAL(12,6)

);

```



\## Notable SQL



A self-join computing each country's % change in coal emissions between two years:



```sql

SELECT a.Country, a.Coal AS StartCoal, b.Coal AS EndCoal,

&#x20;      ROUND(((b.Coal - a.Coal) / a.Coal) \* 100, 2) AS PctChange

FROM emission a

JOIN emission b ON a.Country = b.Country

WHERE a.Year = 2000 AND b.Year = 2024

ORDER BY PctChange ASC

LIMIT 10;

```



\## License



MIT

