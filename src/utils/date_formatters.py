from datetime import datetime

def format_db_date(dt: datetime) -> str:
    """format_db_date — Converts datetime to standard YYYY-MM-DD."""
    return dt.strftime("%Y-%m-%d")
