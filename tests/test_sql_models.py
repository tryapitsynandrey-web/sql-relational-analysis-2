import pytest
import os
import sys
import duckdb
import pandas as pd

# Ensure src in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db.db_client import DBClient

@pytest.fixture(scope="module")
def integration_db():
    """Spins up an entirely isolated in-memory DuckDB for complex SQL model testing."""
    test_db_path = "data/integration_test.db"
    
    # Ensure clean slate
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
        
    client = DBClient(test_db_path, read_only=False)
    
    # Initial Schema Setup
    with client._get_connection() as conn:
        conn.execute("""
            CREATE TABLE events (
                session_id VARCHAR,
                user_id VARCHAR,
                event_type VARCHAR,
                product_id VARCHAR,
                price DECIMAL,
                timestamp TIMESTAMP
            )
        """)
        
        # Inject carefully mathematical explicit mock records into the database
        conn.execute("""
            INSERT INTO events VALUES
            -- Session 1: View to Cart (No Purchase) - Abandonment Case
            ('S1', 'U1', 'view', 'P1', 10.0, '2025-01-01 10:00:00'),
            ('S1', 'U1', 'cart', 'P1', 10.0, '2025-01-01 10:05:00'),
            
            -- Session 2: View to Cart to Purchase (Success Case)
            ('S2', 'U2', 'view', 'P2', 50.0, '2025-01-02 11:00:00'),
            ('S2', 'U2', 'cart', 'P2', 50.0, '2025-01-02 11:02:00'),
            ('S2', 'U2', 'purchase', 'P2', 50.0, '2025-01-02 11:05:00'),
            
            -- Session 3: Immediate Purchase (Zero Cart) - Edge Case
            ('S3', 'U3', 'purchase', 'P3', 100.0, '2025-01-03 12:00:00');
        """)
        
    yield client
    
    # Teardown
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

def test_cart_abandonment_integration(integration_db):
    """Integration test asserting the complex mathematical reality of the cart abandonment model."""
    sql_path = "src/models/marts/cart_abandonment_rate.sql"
    
    # Execute the actual production SQL file against the fully mocked in-memory database
    df = integration_db.execute_file(sql_path)
    
    # Assertions based on our strict data injection
    assert not df.empty
    
    # We expect 2 distinct days of cart activity (S1 on 01-01 and S2 on 01-02). S3 had no cart.
    assert len(df) == 2 
    
    # Assert 01-01 (S1) behavior
    row_01 = df[df['act_date'] == pd.Timestamp('2025-01-01')]
    assert row_01.iloc[0]['abandoned_carts'] == 1
    assert row_01.iloc[0]['cart_abandonment_rate'] == 100.0
    
    # Assert 01-02 (S2) behavior
    row_02 = df[df['act_date'] == pd.Timestamp('2025-01-02')]
    assert row_02.iloc[0]['abandoned_carts'] == 0
    assert row_02.iloc[0]['cart_abandonment_rate'] == 0.0

def test_view_to_cart_funnel_integration(integration_db):
    """Integration test asserting funnel aggregate drop-off math logic."""
    sql_path = "src/models/marts/view_to_cart_funnel.sql"
    
    df = integration_db.execute_file(sql_path)
    
    assert not df.empty
    
    # Validate the macro percentages across the entire system mock
    # Total Views = 2. Carts from Views = 2. Rate = 100%
    assert df.iloc[0]['view_to_cart_rate'] == 100.0
    
    # Total Carts = 2 (S1 and S2). Purchases from those Carts = 1 (S2).
    # S3 is a direct purchase, so it doesn't count towards the cart_to_purchase_rate.
    # Therefore, cart_to_purchase_rate = 1 / 2 = 50.0%
    assert df.iloc[0]['cart_to_purchase_rate'] == 50.0
