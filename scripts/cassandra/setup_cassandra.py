from cassandra.cluster import Cluster

def create_schema():
    cluster = Cluster(['cassandra'])  # container name
    session = cluster.connect()

    # Create keyspace
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS ad_analytics
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
    """)
    session.set_keyspace("ad_analytics")

    # Q1 - CTR per campaign per day
    session.execute("""
        CREATE TABLE IF NOT EXISTS campaign_stats_by_day (
            campaign_id INT,
            day DATE,
            impressions INT,
            clicks INT,
            PRIMARY KEY ((campaign_id), day)
        ) WITH CLUSTERING ORDER BY (day DESC)
    """)

    # Q2 + Q5 - Spend per advertiser, per day, per region
    session.execute("""
        CREATE TABLE IF NOT EXISTS advertiser_spend_by_day (
            advertiser_id INT,
            day DATE,
            region TEXT,
            spend DECIMAL,
            PRIMARY KEY ((region, day), spend, advertiser_id)
        ) WITH CLUSTERING ORDER BY (spend DESC)
    """)

    # Q3 - Last 10 ads seen by user
    session.execute("""
        CREATE TABLE IF NOT EXISTS user_ad_events (
            user_id INT,
            event_time TIMESTAMP,
            ad_id INT,
            was_clicked BOOLEAN,
            PRIMARY KEY ((user_id), event_time)
        ) WITH CLUSTERING ORDER BY (event_time DESC)
    """)

    # Q4 - Top 10 users by clicks per day
    session.execute("""
        CREATE TABLE IF NOT EXISTS user_clicks_by_day (
            day DATE,
            clicks INT,
            user_id INT,
            PRIMARY KEY ((day), clicks, user_id)
        ) WITH CLUSTERING ORDER BY (clicks DESC)
    """)

    print("Cassandra schemas created successfully.")

if __name__ == "__main__":
    create_schema()
