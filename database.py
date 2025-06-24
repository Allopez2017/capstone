import sqlite3
import pandas as pd

def load_and_clean_data(csv_path="world_series.csv"):
    df = pd.read_csv(csv_path, usecols=[0, 1, 2])
    df.columns = ["Year", "Winner", "Loser"]
    df.dropna(subset=["Year", "Winner", "Loser"], inplace=True)
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df.dropna(subset=["Year"], inplace=True)
    df["Year"] = df["Year"].astype("int")
    df.drop_duplicates(subset=["Year", "Winner", "Loser"], inplace=True)
    return df

def insert_into_db(df, db_path="world_series.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS world_series (
            year INTEGER,
            winner TEXT,
            loser TEXT,
            UNIQUE(year, winner, loser)
        )
    """)
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT OR IGNORE INTO world_series (year, winner, loser)
            VALUES (?, ?, ?)
        """, (row['Year'], row['Winner'], row['Loser']))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    df = load_and_clean_data()
    insert_into_db(df)

