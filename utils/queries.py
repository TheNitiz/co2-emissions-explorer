from utils.db import run_query

TABLE = "emission"


def get_global_yearly_totals():
    sql = f"""
        SELECT Year, SUM(Total) AS GlobalTotal
        FROM {TABLE}
        WHERE Total IS NOT NULL AND Country <> 'Global'
        GROUP BY Year
        ORDER BY Year;
    """
    return run_query(sql)


def get_summary_stats():
    """Headline KPIs for the landing page."""
    sql = f"""
        SELECT
            (SELECT MAX(Year) FROM {TABLE} WHERE Country <> 'Global') AS LatestYear,
            (SELECT SUM(Total) FROM {TABLE}
                WHERE Year = (SELECT MAX(Year) FROM {TABLE} WHERE Country <> 'Global')
                AND Country <> 'Global') AS TotalLatest,
            (SELECT SUM(Total) FROM {TABLE}
                WHERE Year = (SELECT MAX(Year) FROM {TABLE} WHERE Country <> 'Global') - 1
                AND Country <> 'Global') AS TotalPrevious,
            (SELECT Country FROM {TABLE}
                WHERE Year = (SELECT MAX(Year) FROM {TABLE} WHERE Country <> 'Global')
                AND Country <> 'Global'
                ORDER BY Total DESC LIMIT 1) AS TopEmitterLatest;
    """
    return run_query(sql)


def get_map_data(min_year=1900):
    """Country-year emissions data for the animated choropleth map."""
    sql = f"""
        SELECT Country, ISO3, Year, Total, PerCapita
        FROM {TABLE}
        WHERE Year >= {min_year}
          AND ISO3 IS NOT NULL
          AND Total IS NOT NULL
          AND Country <> 'Global';
    """
    return run_query(sql)


def get_country_list():
    """Distinct list of countries for dropdowns/multiselects."""
    sql = f"SELECT DISTINCT Country FROM {TABLE} WHERE Country <> 'Global' ORDER BY Country;"
    return run_query(sql)


def get_country_comparison(countries: list, metric: str = "Total"):
    """Yearly trend for selected countries and a chosen metric."""
    allowed_metrics = {"Total", "Coal", "Oil", "Gas", "Cement", "Flaring", "Other", "PerCapita"}
    if metric not in allowed_metrics:
        raise ValueError(f"Invalid metric: {metric}")

    placeholders = ", ".join(f"'{c}'" for c in countries)
    sql = f"""
        SELECT Country, Year, {metric} AS Value
        FROM {TABLE}
        WHERE Country IN ({placeholders})
          AND {metric} IS NOT NULL
        ORDER BY Country, Year;
    """
    return run_query(sql)


def get_fuel_mix(country: str):
    """Fuel-type breakdown over time for one country."""
    sql = f"""
        SELECT Year, Coal, Oil, Gas, Cement, Flaring, Other
        FROM {TABLE}
        WHERE Country = '{country}'
        ORDER BY Year;
    """
    return run_query(sql)


def get_top_emitters(year: int, limit: int = 10):
    sql = f"""
        SELECT Country, Total, PerCapita
        FROM {TABLE}
        WHERE Year = {year} AND Total IS NOT NULL AND Country <> 'Global'
        ORDER BY Total DESC
        LIMIT {limit};
    """
    return run_query(sql)


def get_fastest_decliners(start_year: int, end_year: int, limit: int = 10):
    """Countries with the largest % decline in Coal emissions over a period."""
    sql = f"""
        SELECT
            a.Country,
            a.Coal AS StartCoal,
            b.Coal AS EndCoal,
            ROUND(((b.Coal - a.Coal) / a.Coal) * 100, 2) AS PctChange
        FROM {TABLE} a
        JOIN {TABLE} b
          ON a.Country = b.Country
        WHERE a.Year = {start_year}
          AND b.Year = {end_year}
          AND a.Coal IS NOT NULL AND a.Coal > 0
          AND b.Coal IS NOT NULL
          AND a.Country <> 'Global'
        ORDER BY PctChange ASC
        LIMIT {limit};
    """
    return run_query(sql)


def get_country_peak_year(country: str):
    """The year a country's Total emissions peaked."""
    sql = f"""
        SELECT Year, Total
        FROM {TABLE}
        WHERE Country = '{country}' AND Total IS NOT NULL
        ORDER BY Total DESC
        LIMIT 1;
    """
    return run_query(sql)