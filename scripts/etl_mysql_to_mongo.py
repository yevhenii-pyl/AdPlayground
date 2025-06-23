from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
from collections import defaultdict
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

# Configs
BATCH_SIZE = 1000

# SQLAlchemy setup (streaming mode)
user = os.getenv("MYSQL_USER", "root")
password = os.getenv("MYSQL_PASSWORD", "pass")
host = os.getenv("MYSQL_HOST", "localhost")
port = int(os.getenv("MYSQL_PORT", 3306))
db = os.getenv("MYSQL_DATABASE", "ad_db")
DB_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
engine = create_engine(DB_URL, execution_options={"stream_results": True})

# Mongo setup
mongo = MongoClient(os.getenv("MONGO_URI"))
mdb = mongo["ad_analytics"]
users_collection = mdb["users"]

# Query
QUERY = """
SELECT 
  u.id AS user_id,
  u.age,
  g.label AS gender,
  l.name AS location,
  GROUP_CONCAT(DISTINCT i.name) AS interests,
  ae.timestamp,
  d.type AS device,
  ass.size AS ad_slot_size,
  c.name AS campaign_name,
  c.advertiser_id,
  ae.was_clicked,
  ae.click_timestamp,
  ae.ad_cost,
  ae.ad_revenue,
  c.budget,
  c.remaining_budget
FROM users u
JOIN genders g ON u.gender_id = g.id
JOIN locations l ON u.location_id = l.id
LEFT JOIN user_interests ui ON u.id = ui.user_id
LEFT JOIN interests i ON ui.interest_id = i.id
JOIN ad_events ae ON ae.user_id = u.id
JOIN campaigns c ON ae.campaign_id = c.id
JOIN ad_slot_sizes ass ON ae.ad_slot_size_id = ass.id
JOIN devices d ON ae.device_id = d.id
GROUP BY ae.id
"""

# Helper to flush users to Mongo
def flush_to_mongo(user_map, total_inserted):
    bulk = list(user_map.values())
    if not bulk:
        return total_inserted

    users_collection.insert_many(bulk)
    print(f"Inserted {len(bulk)} users... (Total: {total_inserted + len(bulk)})")
    return total_inserted + len(bulk)

# Main ETL loop
with engine.connect() as conn:
    result = conn.execution_options(stream_results=True).execute(text(QUERY))

    user_map = defaultdict(lambda: {
        "user_id": None,
        "age": None,
        "gender": None,
        "location": None,
        "interests": [],
        "engagement_history": []
    })

    seen_users = set()
    inserted_total = 0

    for row in result:
        uid = row.user_id
        if uid not in seen_users and len(seen_users) >= BATCH_SIZE:
            inserted_total = flush_to_mongo(user_map, inserted_total)
            user_map.clear()
            seen_users.clear()

        seen_users.add(uid)
        user_doc = user_map[uid]
        user_doc["user_id"] = uid
        user_doc["age"] = row.age
        user_doc["gender"] = row.gender
        user_doc["location"] = row.location
        user_doc["interests"] = [i.strip() for i in row.interests.split(",")] if row.interests else []

        user_doc["engagement_history"].append({
            "timestamp": row.timestamp,
            "device": row.device,
            "ad_slot_size": row.ad_slot_size,
            "campaign_name": row.campaign_name,
            "advertiser_id": row.advertiser_id,
            "was_clicked": row.was_clicked,
            "click_timestamp": row.click_timestamp,
            "ad_cost": row.ad_cost,
            "ad_revenue": row.ad_revenue,
            "budget": row.budget,
            "remaining_budget": row.remaining_budget
        })

    # Final flush
    inserted_total = flush_to_mongo(user_map, inserted_total)
    print(f"Done. Total users inserted: {inserted_total}")
# Close Mongo connection