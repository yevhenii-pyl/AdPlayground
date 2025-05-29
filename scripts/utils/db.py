import os
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DB"),
}

def get_engine():
    return create_engine(
        f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )

def load_dataframe(df, table_name: str):
    engine = get_engine()
    df.to_sql(table_name, con=engine, if_exists="append", index=False)
    print(f"✅ Inserted {len(df)} rows into '{table_name}'")

def has_already_run(seed_name: str) -> bool:
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT COUNT(*) FROM seed_status WHERE name = :name"),
            {"name": seed_name}
        )
        return result.scalar() > 0

def mark_seed_as_run(seed_name: str):
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO seed_status (name, ran_at) VALUES (:name, :ran_at)"),
            {"name": seed_name, "ran_at": datetime.utcnow()}
        )
        conn.commit()