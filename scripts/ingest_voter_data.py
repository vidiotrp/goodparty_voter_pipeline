import pandas as pd
import requests
import os
from io import StringIO
from sqlalchemy import create_engine, text

def ingest_voter_data():
    # --- 1. CSV URL ---
    csv_url = "https://gist.githubusercontent.com/hhkarimi/03b7d159478b319679e308e252f58d44/raw/27538c61b73194f921f339c4dbde3f0360918ec1/goodparty-data-engineering-case-study-data.csv"
    
    # --- 2. Download CSV ---
    r = requests.get(csv_url)
    r.raise_for_status()
    df = pd.read_csv(StringIO(r.text))
    
    # --- 3. Clean column names ---
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    df = df.rename(columns={'id': 'voter_id'})
    
    # --- 4. Connect to Postgres (inside Docker) ---
    pg_user = os.getenv('POSTGRES_USER', 'airflow')
    pg_pass = os.getenv('POSTGRES_PASSWORD', 'airflow')
    pg_db   = os.getenv('POSTGRES_DB', 'goodparty')
    pg_host = os.getenv('POSTGRES_HOST', 'postgres')  # default Docker service hostname
    pg_port = os.getenv('POSTGRES_PORT', '5432')
    
    engine = create_engine(f"postgresql+psycopg2://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}")
    
    # --- 5. Create staging table if it doesn't exist ---
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS voter_staging (
        voter_id TEXT PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        age INT,
        gender TEXT,
        state TEXT,
        party TEXT,
        email TEXT,
        registered_date DATE,
        last_voted_date DATE,
        updated_at DATE
    )
    """
    with engine.begin() as conn:
        conn.execute(text(create_table_sql))
    
    # --- 6. Fetch existing voter_ids ---
    existing_ids = pd.read_sql("SELECT voter_id FROM voter_staging", engine)
    
    # --- 7. Filter only new rows ---
    new_rows = df[~df['voter_id'].isin(existing_ids['voter_id'])]
    
    # --- 8. Insert new rows if any ---
    if not new_rows.empty:
        new_rows.to_sql("voter_staging", engine, if_exists="append", index=False)
        print(f"Ingested {len(new_rows)} new rows.")
    else:
        print("No new rows to ingest.")

# --- 9. Run ingestion ---
if __name__ == "__main__":
    ingest_voter_data()
