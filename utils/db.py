import os
import ssl
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()


def get_secret(key):
    try:
        return st.secrets[key]
    except (KeyError, FileNotFoundError):
        return os.getenv(key)


DB_HOST = get_secret("DB_HOST")
DB_PORT = get_secret("DB_PORT")
DB_USER = get_secret("DB_USER")
DB_PASSWORD = get_secret("DB_PASSWORD")
DB_NAME = get_secret("DB_NAME")


@st.cache_resource
def get_engine():
    """Create and cache a single database engine for the app's lifetime."""
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    connection_string = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(connection_string, connect_args={"ssl": ssl_context})


@st.cache_data(ttl=3600)
def run_query(sql: str) -> pd.DataFrame:
    """Run a SQL query and return the result as a DataFrame. Cached for 1 hour."""
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(sql, conn)