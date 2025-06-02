import pandas as pd
import uuid
from sqlalchemy import create_engine, text

DB_URL = "mysql+pymysql://root:pass@localhost:3306/ad_db"
engine = create_engine(DB_URL)


def load_campaign_map():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, name FROM campaigns")).mappings()
        lookup = {}
        for row in result:
            name = row["name"]
            if name:
                lookup[name.strip().lower()] = row["id"]
        return lookup


def load_lookup_table(table_name, key_col):
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT id, {key_col} FROM {table_name}")).mappings()
        lookup = {}
        for row in result:
            key_value = row[key_col]
            if key_value:
                lookup[key_value.strip().lower()] = row["id"]
        return lookup


def preprocess_chunk(chunk: pd.DataFrame, campaign_map, ad_slot_map, device_map, location_map) -> pd.DataFrame:
    chunk = chunk.rename(columns={
        "EventID": "id",
        "UserID": "user_id",
        "Timestamp": "timestamp",
        "BidAmount": "bid_amount",
        "AdCost": "ad_cost",
        "WasClicked": "was_clicked",
        "ClickTimestamp": "click_timestamp",
        "AdRevenue": "ad_revenue",
    })

    chunk["campaign_id"] = chunk["CampaignName"].str.strip().str.lower().map(campaign_map)
    chunk["ad_slot_size_id"] = chunk["AdSlotSize"].str.strip().str.lower().map(ad_slot_map)
    chunk["device_id"] = chunk["Device"].str.strip().str.lower().map(device_map)
    chunk["location_id"] = chunk["Location"].str.strip().str.lower().map(location_map)

    chunk["user_id"] = chunk["user_id"].astype(int)

    # Генеруємо унікальний UUID для id, якщо він є пустий або треба новий
    chunk["id"] = [str(uuid.uuid4()) for _ in range(len(chunk))]

    # Відбираємо потрібні колонки
    cols = [
        "id", "campaign_id", "ad_slot_size_id", "user_id",
        "device_id", "location_id", "timestamp", "bid_amount",
        "ad_cost", "was_clicked", "click_timestamp", "ad_revenue"
    ]

    chunk = chunk[cols]

    before_drop = len(chunk)
    chunk = chunk.dropna(subset=["campaign_id", "ad_slot_size_id", "user_id", "device_id", "location_id"])
    dropped = before_drop - len(chunk)
    if dropped > 0:
        print(f"⚠️ Dropped {dropped} rows due to missing FK mappings")

    return chunk


def insert_chunk(df):
    if df.empty:
        print("⚠️ No rows to insert in this chunk.")
        return
    with engine.connect() as conn:
        df.to_sql('ad_events', con=conn, if_exists='append', index=False)
    print(f"✅ Inserted {len(df)} rows into 'ad_events'")


def run():
    print("Loading campaign mappings from DB...")
    campaign_map = load_campaign_map()
    print(f"✅ Loaded {len(campaign_map)} campaigns")

    print("🔧 Loading lookup tables from DB...")
    ad_slot_map = load_lookup_table("ad_slot_sizes", "size")
    print(f"✅ Loaded {len(ad_slot_map)} ad slot sizes")
    device_map = load_lookup_table("devices", "type")
    print(f"✅ Loaded {len(device_map)} devices")
    location_map = load_lookup_table("locations", "name")
    print(f"✅ Loaded {len(location_map)} locations")

    chunksize = 100000
    file_path = "data/ad_events_fixed.csv"  # Твій очищений csv файл
    for i, chunk in enumerate(pd.read_csv(file_path, chunksize=chunksize)):
        print(f"Processing chunk {i+1} with {len(chunk)} rows")
        chunk_processed = preprocess_chunk(chunk, campaign_map, ad_slot_map, device_map, location_map)
        insert_chunk(chunk_processed)


if __name__ == "__main__":
    run()
