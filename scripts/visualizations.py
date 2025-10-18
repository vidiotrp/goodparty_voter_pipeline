import os
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# --- 1. Connect to Postgres ---
engine = create_engine(
    f"postgresql+psycopg2://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@localhost:5432/{os.environ['POSTGRES_DB']}"
)

# --- 2. Load marts ---
state_df = pd.read_sql("SELECT * FROM voter_county_by_state", engine)
state_df = state_df[state_df['state'].notna() & (state_df['state'] != '')]
party_df = pd.read_sql("SELECT * FROM party_affiliation_distribution", engine)

# --- 3. Visualization: Voter count by state ---
plt.figure(figsize=(10, 6))
plt.bar(state_df['state'], state_df['total_voters'], color='skyblue')
plt.ylim(state_df['total_voters'].min() * 0.95, state_df['total_voters'].max() * 1.05)
plt.title("Voter Count by State")
plt.ylabel("Number of Voters")
plt.xlabel("State")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/voter_count_by_state.png")
plt.show()

# --- 4. Visualization: Male vs Female voters by state ---
plt.figure(figsize=(10, 6))
plt.bar(state_df['state'], state_df['male_voters'], label='Male', alpha=0.7)
plt.bar(state_df['state'], state_df['female_voters'], bottom=state_df['male_voters'], label='Female', alpha=0.7)
plt.title("Male vs Female Voters by State")
plt.ylabel("Number of Voters")
plt.xlabel("State")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/voter_gender_by_state.png")
plt.show()

# --- 5. Visualization: Party affiliation distribution ---
plt.figure(figsize=(10, 6))
plt.bar(party_df['party'], party_df['total_voters'], color='lightgreen')
plt.title("Total Voters by Party")
plt.ylabel("Number of Voters")
plt.xlabel("Party")
plt.tight_layout()
plt.savefig("charts/voter_count_by_party.png")
plt.show()

# --- 6. Visualization: Missing emails by party ---
plt.figure(figsize=(10, 6))
plt.bar(party_df['party'], party_df['missing_email'], color='salmon')
plt.title("Voters Missing Emails by Party")
plt.ylabel("Count of Missing Emails")
plt.xlabel("Party")
plt.tight_layout()
plt.savefig("charts/missing_emails_by_party.png")
plt.show()

# --- 7. Visualization: Voters not voted in last year by party ---
plt.figure(figsize=(10, 6))
plt.bar(party_df['party'], party_df['not_voted_last_year'], color='orange')
plt.title("Voters Not Voted in Last Year by Party")
plt.ylabel("Number of Voters")
plt.xlabel("Party")
plt.tight_layout()
plt.savefig("charts/not_voted_last_year_by_party.png")
plt.show()
