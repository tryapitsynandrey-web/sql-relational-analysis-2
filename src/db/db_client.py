import duckdb
import pandas as pd
from typing import Optional
from src.utils.logger import get_logger

logger = get_logger("db_client")

class DBClient:
    """DBClient — Manages DuckDB connection and query execution."""
    
    def __init__(self, db_path: str = "data/analytics.db", read_only: bool = True):
        self.db_path = db_path
        self.read_only = read_only
        
    def _get_connection(self):
        # read_only=True prevents file locking crashes during concurrent Streamlit user sessions
        # Pytest requires write access to build test schemas
        import os
        # Fallback to write mode if the DB doesn't exist yet, avoiding IO errors
        ro = self.read_only if os.path.exists(self.db_path) else False
        return duckdb.connect(self.db_path, read_only=ro)
        
    def execute_query(self, query: str) -> pd.DataFrame:
        """execute_query — Executes raw SQL and returns a stateless pandas DataFrame."""
        try:
            with self._get_connection() as conn:
                df = conn.execute(query).df()
            return df
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
            
    def execute_file(self, file_path: str) -> pd.DataFrame:
        """execute_file — Reads a SQL file and executes it."""
        try:
            with open(file_path, "r") as f:
                query = f.read()
            return self.execute_query(query)
        except Exception as e:
            logger.error(f"Failed to execute SQL file {file_path}: {e}")
            raise
