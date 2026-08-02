import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

CSV_PATH = "C:/Users/nitiz/Downloads/co2_emits.csv"

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?ssl_verify_cert=false"
)

print("Reading CSV...")
df = pd.read_csv(CSV_PATH)

df = df.rename(columns={
    "ISO 3166-1 alpha-3": "ISO3",
    "Per Capita": "PerCapita",
})

print(f"Loaded {len(df)} rows. Inserting into database...")

df.to_sql(
    "emission",
    con=engine,
    if_exists="append",
    index=False,
    chunksize=5000,
    method="multi",
)

print("Done.")