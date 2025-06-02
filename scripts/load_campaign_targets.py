import pandas as pd
import re
from utils.db import get_engine, load_dataframe
from sqlalchemy import text

def get_reference_sets():
    engine = get_engine()
    with engine.connect() as conn:
        interests = {name.lower(): id for id, name in conn.execute(text("SELECT id, name FROM interests"))}
        locations = {name.lower(): id for id, name in conn.execute(text("SELECT id, name FROM locations"))}
    return interests, locations

def extract_campaign_targets(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path, usecols=["CampaignID", "TargetingCriteria"])
    interests_map, locations_map = get_reference_sets()
    records = []

    for _, row in df.iterrows():
        campaign_id = row["CampaignID"]
        criteria = str(row["TargetingCriteria"]).lower()

        # 1. Age range
        min_age, max_age = None, None
        age_match = re.search(r"age\s*(\d+)\s*-\s*(\d+)", criteria)
        if age_match:
            min_age, max_age = map(int, age_match.groups())
            criteria = criteria.replace(age_match.group(0), "")

        # 2. Remaining tokens
        tokens = [i.strip() for i in criteria.split(",") if i.strip()]
        interest_id = None
        location_id = None

        for token in tokens:
            if not interest_id and token in interests_map:
                interest_id = interests_map[token]
            elif not location_id and token in locations_map:
                location_id = locations_map[token]

        records.append({
            "campaign_id": campaign_id,
            "interest_id": interest_id,
            "location_id": location_id,
            "min_age": min_age,
            "max_age": max_age
        })

    return pd.DataFrame(records)


if __name__ == "__main__":
    df = extract_campaign_targets("data/campaigns.csv")
    load_dataframe(df, "campaign_targets")
    print(f"✅ Inserted {len(df)} campaign target rows into DB")
