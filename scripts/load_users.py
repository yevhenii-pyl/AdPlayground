import pandas as pd
from sqlalchemy import text
from utils.db import load_dataframe
from utils.map_lookup_values import map_lookup_values

def extract_users(users_csv: str) -> pd.DataFrame:
    df = pd.read_csv(users_csv, usecols=["UserID", "Age", "Gender", "Location", "SignupDate"])

    df.rename(columns={
        "UserID": "id",
        "Age": "age",
        "SignupDate": "signup_date"
    }, inplace=True)

    # Map genders and locations to their IDs
    df["gender_id"] = map_lookup_values(df, "Gender", "genders", "label")
    df["location_id"] = map_lookup_values(df, "Location", "locations", "name")

    # Drop original textual columns
    df.drop(columns=["Gender", "Location"], inplace=True)

    # Parse date
    df["signup_date"] = pd.to_datetime(df["signup_date"]).dt.date

    return df

if __name__ == "__main__":
    users_df = extract_users("data/users.csv")
    load_dataframe(users_df, "users")
    print("✅ Users inserted into DB")
