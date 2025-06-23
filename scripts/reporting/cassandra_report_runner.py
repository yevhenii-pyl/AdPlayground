import os
import csv
from pathlib import Path
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from datetime import datetime
from collections import defaultdict

CASSANDRA_HOST = os.getenv("CASSANDRA_HOST")
CASSANDRA_PORT = int(os.getenv("CASSANDRA_PORT"))
CASSANDRA_KEYSPACE = os.getenv("CASSANDRA_KEYSPACE")
CASSANDRA_USER = os.getenv("CASSANDRA_USER")
CASSANDRA_PASSWORD = os.getenv("CASSANDRA_PASSWORD")

auth_provider = PlainTextAuthProvider(CASSANDRA_USER, CASSANDRA_PASSWORD)
cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT, auth_provider=auth_provider)
session = cluster.connect(CASSANDRA_KEYSPACE)

def run_cql_to_csv(query_path: str, output_csv: str, params: tuple = ()):
    print(f">>> Running query from: {query_path}")
    print(f"    Params: {params}")

    with open(query_path, "r") as f:
        query = f.read().strip() 

    print("QUERY STRING:", query)
    print("PARAMS:", params)

    expected_params = query.count("%s")
    if expected_params != len(params):
        raise ValueError(f"Query in {query_path} expects {expected_params} params, but got {len(params)}")

    result = session.execute(query, params) if expected_params > 0 else session.execute(query)
    rows = list(result)

    Path("reports").mkdir(exist_ok=True)
    with open(output_csv, "w", newline="") as f:
        if rows:
            writer = csv.DictWriter(f, fieldnames=rows[0]._fields)
            writer.writeheader()
            writer.writerows([row._asdict() for row in rows])
        else:
            print(f"No data returned for {output_csv}")

    print(f"[{datetime.now()}] Generated: {output_csv}")


def run_clicks_aggregation(query_path: str, output_csv: str):
    print(f">>> Running aggregation query from: {query_path}")

    with open(query_path, "r") as f:
        query = f.read().strip()

    result = session.execute(query)
    rows = list(result)

    click_map = defaultdict(int)
    for row in rows:
        click_map[row.user_id] += row.clicks

    top_users = sorted(click_map.items(), key=lambda x: x[1], reverse=True)[:10]

    Path("reports").mkdir(exist_ok=True)
    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["user_id", "total_clicks"])
        writer.writeheader()
        for user_id, total_clicks in top_users:
            writer.writerow({"user_id": user_id, "total_clicks": total_clicks})

    print(f"[{datetime.now()}] Aggregated Top 10 Users: {output_csv}")

queries = [
    ("queries/cassandra/001_ctr_per_campaign_per_day.cql",         "reports/t4/q1_ctr_per_campaign.csv"),
    ("queries/cassandra/002_top5_advertisers_total_spend_30d.cql", "reports/t4/q2_top_advertisers_30d.csv"),
    ("queries/cassandra/003_user_last10_ads.cql",                  "reports/t4/q3_last_10_ads_seen.csv"), 
    ("queries/cassandra/004_top10_users_clicks_30d.cql",           "reports/t4/q4_top_clickers_30d.csv"),
    ("queries/cassandra/005_top5_advertisers_by_region_30d.cql",   "reports/t4/q5_top_advertisers_by_region.csv")
]

params_map = {
    "003_user_last10_ads.cql": (223617,),              
    "005_top5_advertisers_by_region_30d.cql": ("India",),
}

for query_path, output_csv in queries:
    filename = Path(query_path).name

    if filename == "004_top10_users_clicks_30d.cql":
        run_clicks_aggregation(query_path, output_csv)
    else:
        params = params_map.get(filename, ())
        run_cql_to_csv(query_path, output_csv, params)