import pandas as pd
from utils.db import load_dataframe

def extract_interests(user_csv: str) -> pd.DataFrame:
    users = pd.read_csv(user_csv, usecols=["Interests"])

    # Split and clean interests
    raw = (
        users["Interests"]
        .dropna()
        .str.split(",")
        .explode()
        .str.strip()
        .str.title()
    )

    cleaned = raw[raw != ""].drop_duplicates().dropna()

    df = pd.DataFrame({"name": cleaned})
    df["identifier"] = df["name"].str.lower().str.replace(" ", "_")

    return df

if __name__ == "__main__":
    interests_df = extract_interests("data/users.csv")
    load_dataframe(interests_df, "interests")
    print("✅ Interests inserted into DB")
