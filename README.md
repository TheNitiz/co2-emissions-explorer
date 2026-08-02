# 🌍 Global CO2 Emissions Explorer

An interactive data explorer covering 270+ years of global CO2 emissions,
built end-to-end: cloud MySQL database → Python data pipeline → deployed
Streamlit + Plotly app.

**[🔗 Live App](https://your-app-name.streamlit.app)**

![Landing page screenshot](assets/screenshot-home.png)

## Features

- 🗺️ **Animated choropleth map** — watch emissions evolve across 190+ countries, year by year
- 📈 **Country comparison** — compare any countries across any metric (Total, Coal, Oil, Gas, Cement, Flaring, Per Capita)
- 🔥 **Fuel mix breakdown** — see how a country's energy sources have shifted over time
- 🏆 **Leaderboard** — top emitters by year, and fastest coal-decliners via a SQL self-join
- 📊 **Full data matrix** — exportable country × year grid for any metric

## Tech Stack

| Layer | Tool |
|---|---|
| Database | MySQL (hosted on Aiven) |
| Data pipeline | Python, pandas, SQLAlchemy |
| Frontend | Streamlit + Plotly |
| Deployment | Streamlit Community Cloud |

## Data Source

Data from the **Global Carbon Project's Global Carbon Budget** (Friedlingstein et al.,
2025, ESSD). See [ABOUT.md](ABOUT.md) or the in-app About page for full citation
and fair-use details.

## Architecture

CSV (Global Carbon Budget) \
↓ Python import script (pandas + SQLAlchemy) \
MySQL on Aiven \
↓ SQLAlchemy + pymysql, cached queries \ 
Streamlit app (5 pages) → deployed on Streamlit Cloud

## Local Setup

```bash
git clone https://github.com/TheNitiz/co2-emissions-explorer.git
cd co2-emissions-explorer
python -m venv venv
source venv/Scripts/activate   # Windows Git Bash
pip install -r requirements.txt
```

Create a `.env` file with your own database credentials:

DB_HOST=... /
DB_PORT=... /
DB_USER=... /
DB_PASSWORD=... /
DB_NAME=carbon

Run:
```bash
streamlit run Home.py
```

## Database Schema

```sql
CREATE TABLE emission (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    Country       VARCHAR(100),
    ISO3          CHAR(3),
    Year          SMALLINT,
    Total         DECIMAL(12,6),
    Coal          DECIMAL(12,6),
    Oil           DECIMAL(12,6),
    Gas           DECIMAL(12,6),
    Cement        DECIMAL(12,6),
    Flaring       DECIMAL(12,6),
    Other         DECIMAL(12,6),
    PerCapita     DECIMAL(12,6)
);
```

## Notable SQL

A self-join computing each country's % change in coal emissions between two years:

```sql
SELECT a.Country, a.Coal AS StartCoal, b.Coal AS EndCoal,
       ROUND(((b.Coal - a.Coal) / a.Coal) * 100, 2) AS PctChange
FROM emission a
JOIN emission b ON a.Country = b.Country
WHERE a.Year = 2000 AND b.Year = 2024
ORDER BY PctChange ASC
LIMIT 10;
```

## License

MIT
