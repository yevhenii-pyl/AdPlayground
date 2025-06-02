import pandas as pd
from utils.db import load_dataframe

def extract_advertisers(campaign_csv: str) -> pd.DataFrame:
    campaigns = pd.read_csv(campaign_csv, usecols=["AdvertiserName"])

    raw = campaigns["AdvertiserName"].dropna().str.strip()
    cleaned = raw[raw != ""].drop_duplicates().dropna()

    df = pd.DataFrame({"name": cleaned})

    return df

if __name__ == "__main__":
    advertisers_df = extract_advertisers("data/campaigns.csv")
    load_dataframe(advertisers_df, "advertisers")
    print("✅ Advertisers inserted into DB")
