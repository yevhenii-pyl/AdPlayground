from sqlalchemy import create_engine, text
from cassandra.cluster import Cluster
from cassandra.concurrent import execute_concurrent_with_args
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import os

load_dotenv()

# --- MySQL Setup ---
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST")
port = int(os.getenv("MYSQL_PORT"))
db = os.getenv("MYSQL_DATABASE")
DB_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
engine = create_engine(DB_URL)

# --- Cassandra Setup ---
cluster = Cluster(['cassandra'])
session = cluster.connect('ad_analytics')

# --- Seeding Functions ---
def insert_rows(prepared_stmt, rows):
    execute_concurrent_with_args(session, prepared_stmt, rows, concurrency=16)

def seed_campaign_stats():
    query = """
    SELECT * FROM (
        SELECT
            c.id AS campaign_id,
            DATE(ae.timestamp) AS day,
            COUNT(*) AS impressions,
            SUM(ae.was_clicked) AS clicks
        FROM (
            SELECT * FROM ad_events
            ORDER BY RAND()
            LIMIT 50000
        ) ae
        JOIN campaigns c ON ae.campaign_id = c.id
        GROUP BY c.id, DATE(ae.timestamp)
    ) AS grouped
    LIMIT 500;
    """
    with engine.connect() as conn:
        rows = list(conn.execution_options(stream_results=True).execute(text(query)))

    insert_stmt = session.prepare("""
        INSERT INTO campaign_stats_by_day (campaign_id, day, impressions, clicks)
        VALUES (?, ?, ?, ?)
    """)
    rows_args = [(int(c), d, int(i), int(cl)) for (c, d, i, cl) in rows]
    insert_rows(insert_stmt, rows_args)
    print(f"campaign_stats_by_day: {len(rows_args)} rows inserted")

def seed_user_clicks():
    query = """
    SELECT
        DATE(ae.timestamp) AS day,
        COUNT(*) AS clicks,
        ae.user_id
    FROM ad_events ae
    WHERE ae.was_clicked = 1
    GROUP BY DATE(ae.timestamp), ae.user_id
    ORDER BY day DESC, clicks DESC
    LIMIT 500;
    """
    with engine.connect() as conn:
        rows = list(conn.execute(text(query)))

    insert_stmt = session.prepare("""
        INSERT INTO user_clicks_by_day (day, clicks, user_id)
        VALUES (?, ?, ?)
    """)
    rows_args = [(d, int(cl), int(uid)) for (d, cl, uid) in rows]
    insert_rows(insert_stmt, rows_args)
    print(f"user_clicks_by_day: {len(rows_args)} rows inserted")

def seed_user_ad_events():
    query = """
    SELECT
        ae.user_id,
        ae.timestamp,
        ae.campaign_id,
        ae.was_clicked
    FROM ad_events ae
    ORDER BY ae.timestamp DESC
    LIMIT 500;
    """
    with engine.connect() as conn:
        rows = list(conn.execute(text(query)))

    insert_stmt = session.prepare("""
        INSERT INTO user_ad_events (user_id, event_time, ad_id, was_clicked)
        VALUES (?, ?, ?, ?)
    """)
    rows_args = [(int(uid), ts, int(cid), bool(click)) for (uid, ts, cid, click) in rows]
    insert_rows(insert_stmt, rows_args)
    print(f"user_ad_events: {len(rows_args)} rows inserted")

def seed_advertiser_spend():
    query = """
        SELECT
            l.name AS region,
            DATE(ae.timestamp) AS day,
            c.advertiser_id,
            SUM(ae.ad_cost) AS spend
        FROM (
            SELECT * FROM ad_events
            ORDER BY RAND()
            LIMIT 50000
        ) ae
        JOIN users u ON ae.user_id = u.id
        JOIN locations l ON u.location_id = l.id
        JOIN campaigns c ON ae.campaign_id = c.id
        GROUP BY region, day, advertiser_id
        LIMIT 500;
    """ 
    with engine.connect() as conn:
        rows = list(conn.execute(text(query)))

    insert_stmt = session.prepare("""
        INSERT INTO advertiser_spend_by_day (region, day, advertiser_id, spend)
        VALUES (%s, %s, %s, %s)
    """)
    rows_args = [(region, d, float(spend), int(adv_id)) for (adv_id, d, region, spend) in rows]
    insert_rows(insert_stmt, rows_args)
    print(f"advertiser_spend_by_day: {len(rows_args)} rows inserted")

# --- Run All Seeders ---
def main():
    with ThreadPoolExecutor() as executor:
        executor.submit(seed_campaign_stats)
        executor.submit(seed_user_clicks)
        executor.submit(seed_user_ad_events)
        executor.submit(seed_advertiser_spend)

if __name__ == "__main__":
    main()
