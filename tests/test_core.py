import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db.db_client import DBClient
from src.core.data_validator import DataValidator

@pytest.fixture
def test_db():
    db_path = "data/test_analytics.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    client = DBClient(db_path, read_only=False)
    
    with client._get_connection() as conn:
        conn.execute("""
            CREATE TABLE events (
                event_type VARCHAR,
                timestamp TIMESTAMP
            )
        """)
        conn.execute("INSERT INTO events VALUES ('view', CURRENT_TIMESTAMP - INTERVAL 1 DAY)")
        
    yield client
    if os.path.exists(db_path):
        os.remove(db_path)

def test_data_validator_success(test_db):
    validator = DataValidator(test_db)
    assert validator.run_sanity_checks() == True

def test_data_validator_fail_future_date(test_db):
    with test_db._get_connection() as conn:
        conn.execute("INSERT INTO events VALUES ('purchase', CURRENT_TIMESTAMP + INTERVAL 1 DAY)")
        
    validator = DataValidator(test_db)
    assert validator.run_sanity_checks() == False

def test_data_validator_fail_invalid_event(test_db):
    with test_db._get_connection() as conn:
        conn.execute("INSERT INTO events VALUES ('unknown_event', CURRENT_TIMESTAMP - INTERVAL 1 DAY)")
        
    validator = DataValidator(test_db)
    assert validator.run_sanity_checks() == False
