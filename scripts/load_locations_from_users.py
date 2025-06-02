import pandas as pd
from utils.db import load_dataframe

def extract_locations_from_users(csv_path: str) -> pd.DataFrame:
    # Load Location column
    df = pd.read_csv(csv_path, usecols=["Location"])
    
    # Clean and normalize
    df["Location"] = df["Location"].str.strip().str.title()
    df = df.dropna().drop_duplicates()
    
    # Prepare for DB insert
    df = df.rename(columns={"Location": "name"})
    df["identifier"] = df["name"].str.lower().str.replace(" ", "_")
    
    return df

if __name__ == "__main__":
    path = "data/users.csv" 
    loc_df = extract_locations_from_users(path)
    
    print(f"✅ Extracted {len(loc_df)} unique locations")
    load_dataframe(loc_df, "locations")
