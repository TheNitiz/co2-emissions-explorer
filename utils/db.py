import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


@st.cache_resource
def get_engine():
    """Create and cache a single database engine for the app's lifetime."""
    connection_string = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    return create_engine(connection_string)


@st.cache_data(ttl=3600)
def run_query(sql: str) -> pd.DataFrame:
    """Run a SQL query and return the result as a DataFrame. Cached for 1 hour."""
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(sql, conn)