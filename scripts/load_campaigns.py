import pandas as pd
from utils.db import load_dataframe
from utils.map_lookup_values import map_lookup_values

def extract_campaigns(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path, usecols=[
        "CampaignID", "CampaignName", "AdvertiserName", "CampaignStartDate",
        "CampaignEndDate", "AdSlotSize", "Budget", "RemainingBudget"
    ])

    df["advertiser_id"] = map_lookup_values(df, "AdvertiserName", "advertisers", "name")
    df["ad_slot_size_id"] = map_lookup_values(df, "AdSlotSize", "ad_slot_sizes", "size")

    campaigns_df = df.rename(columns={
        "CampaignID": "id",
        "CampaignName": "name",
        "CampaignStartDate": "start_date",
        "CampaignEndDate": "end_date",
        "Budget": "budget",
        "RemainingBudget": "remaining_budget"
    })[[
        "id", "name", "advertiser_id", "start_date", "end_date",
        "ad_slot_size_id", "budget", "remaining_budget"
    ]]

    return campaigns_df.dropna()

if __name__ == "__main__":
    df = extract_campaigns("data/campaigns.csv")
    load_dataframe(df, "campaigns")
    print(f"✅ Inserted {len(df)} campaigns into DB")
