from sqlalchemy import text
import pandas as pd
from .db import get_engine

def map_lookup_values(df: pd.DataFrame, column: str, lookup_table: str, lookup_col: str ) -> pd.Series:
    """
    Maps text values in a dataframe column to foreign key IDs from a lookup table.
    Assumes lookup table has 'id' column.
    """
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT id, {lookup_col} FROM {lookup_table}"))
        mapping = {name.lower(): id for id, name in result.fetchall()}

    return df[column].str.strip().str.lower().map(mapping)
