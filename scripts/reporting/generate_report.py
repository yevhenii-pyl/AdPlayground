import os
import csv
from pathlib import Path
from sqlalchemy import create_engine, text

user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST")
port = int(os.getenv("MYSQL_PORT")) 
db = os.getenv("MYSQL_DATABASE")

DB_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
engine = create_engine(DB_URL)

def run_query_to_csv(query_path, output_csv):
    with engine.connect() as conn:
        with open(query_path, "r") as f:
            sql = f.read()

        result = conn.execute(text(sql))
        rows = result.mappings().all()

        Path("reports").mkdir(exist_ok=True)
        with open(output_csv, "w", newline="") as f:
            if rows:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            else:
                print(f"No data returned for {query_path}")

        print(f"Generated: {output_csv}")

run_query_to_csv("queries/mysql/011_top_ctr_campaigns.sql", "reports/t2/top_ctr_campaigns.csv")
run_query_to_csv("queries/mysql/012_top_spender_efficiency.sql", "reports/t2/top_spender_efficiency.csv")
run_query_to_csv("queries/mysql/021_advertiser_campaign_efficiency.sql", "reports/t2/advertiser_campaign_efficiency.csv")
run_query_to_csv("queries/mysql/031_campaign_cost_efficiency.sql", "reports/t2/campaign_cost_efficiency.csv")
run_query_to_csv("queries/mysql/032_regional_revenue_analysis.sql", "reports/t2/regional_revenue_analysis.csv")
run_query_to_csv("queries/mysql/041_revenue_from_clicks_by_location.sql", "reports/t2/revenue_from_clicks_by_location.csv")
run_query_to_csv("queries/mysql/051_most_engaged_users.sql", "reports/t2/most_engaged_users.csv")
run_query_to_csv("queries/mysql/061_campaigns_near_budget_exhaustion.sql", "reports/t2/campaigns_near_budget_exhaustion.csv")
run_query_to_csv("queries/mysql/071_device_ctr_comparison.sql", "reports/t2/device_ctr_comparison.csv")