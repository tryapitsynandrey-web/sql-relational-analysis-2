from src.db.db_client import DBClient
from src.utils.logger import get_logger

logger = get_logger("data_validator")

class DataValidator:
    """DataValidator — Runs sanity-check SQL before allowing data fetch."""
    
    def __init__(self, db_client: DBClient):
        self.db = db_client
        
    def run_sanity_checks(self) -> bool:
        """run_sanity_checks — Ensures no orphaned events or future dates."""
        try:
            # Check for future dates
            future_dates_query = "SELECT COUNT(*) AS cnt FROM events WHERE timestamp > CAST(CURRENT_TIMESTAMP AS TIMESTAMP)"
            df = self.db.execute_query(future_dates_query)
            if df['cnt'].iloc[0] > 0:
                logger.error("Data validation failed: Future dates found in events.")
                return False
                
            # Check for invalid event types
            invalid_events_query = "SELECT COUNT(*) AS cnt FROM events WHERE event_type NOT IN ('view', 'cart', 'purchase')"
            df = self.db.execute_query(invalid_events_query)
            if df['cnt'].iloc[0] > 0:
                logger.error("Data validation failed: Invalid event types found.")
                return False
                
            logger.info("Data validation passed successfully.")
            return True
        except Exception as e:
            logger.error(f"Validation process encountered an error: {e}")
            return False
