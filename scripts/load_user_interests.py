import pandas as pd
from utils.db import get_engine, load_dataframe
from sqlalchemy import text

def map_interests() -> dict:
    """Returns a map of interest name (lowercase) to interest_id"""
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, name FROM interests"))
        return {name.lower(): id for id, name in result.fetchall()}

def extract_user_interests(user_csv: str) -> pd.DataFrame:
    users = pd.read_csv(user_csv, usecols=["UserID", "Interests"])
    users = users.dropna(subset=["Interests"])

    interests_map = map_interests()

    records = []

    for _, row in users.iterrows():
        user_id = row["UserID"]
        interests = [i.strip().lower() for i in row["Interests"].split(",") if i.strip()]
        for interest in interests:
            if interest in interests_map:
                records.append({"user_id": user_id, "interest_id": interests_map[interest]})
            else:
                print(f"Interest not found in DB: {interest}")

    return pd.DataFrame(records).drop_duplicates()

if __name__ == "__main__":
    df = extract_user_interests("data/users.csv")
    load_dataframe(df, "user_interests")
    print(f"Inserted {len(df)} rows into 'user_interests'")
