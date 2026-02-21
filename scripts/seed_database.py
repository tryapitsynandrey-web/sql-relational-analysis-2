import os
import sys
import random
import duckdb
from datetime import datetime, timedelta

# Ensure src in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils.logger import get_logger

logger = get_logger("seed_database")

DB_PATH = "data/analytics.db"

def seed_database():
    """seed_database — Generates realistic synthetic e-commerce event data."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    logger.info("Connecting to DuckDB...")
    with duckdb.connect(DB_PATH) as conn:
        logger.info("Dropping existing events table if it exists...")
        conn.execute("DROP TABLE IF EXISTS events")
        
        logger.info("Creating events table...")
        conn.execute("""
            CREATE TABLE events (
                event_id VARCHAR,
                session_id VARCHAR,
                user_id VARCHAR,
                timestamp TIMESTAMP,
                event_type VARCHAR,
                product_id VARCHAR,
                price DECIMAL(10, 2)
            )
        """)
        
        logger.info("Generating synthetic data (10k+ rows)...")
        users = [f"u_{i}" for i in range(1000)]
        products = [f"p_{i}" for i in range(100)]
        sessions = [f"s_{i}" for i in range(3000)] # 3000 sessions for 15000 events = 5 items per session avg
        
        start_date = datetime.now() - timedelta(days=90)
        
        # Batch insert for performance
        data = []
        for i in range(15000):
            user = random.choice(users)
            # Pick a session. Tie it roughly to the user so the same user has the same session
            session = random.choice(sessions)
            product = random.choice(products)
            
            # Funnel progression logic
            ts = start_date + timedelta(days=random.randint(0, 90), hours=random.randint(0, 23), minutes=random.randint(0, 59))
            
            # View
            data.append((f"evt_{i}_v", session, user, ts, 'view', product, 0.0))
            
            # 30% chance to cart
            if random.random() < 0.3:
                ts += timedelta(minutes=random.randint(1, 10))
                data.append((f"evt_{i}_c", session, user, ts, 'cart', product, 0.0))
                
                # 40% chance of the carted items to be purchased
                if random.random() < 0.4:
                    ts += timedelta(minutes=random.randint(1, 5))
                    
                    # Simulate true Market Basket (2-5 distinct items purchased together)
                    num_basket_items = random.randint(2, 5)
                    basket_products = random.sample(products, num_basket_items)
                    
                    for j, bp in enumerate(basket_products):
                        # Add each to cart
                        data.append((f"evt_{i}_c_{j}", session, user, ts - timedelta(seconds=10*j), 'cart', bp, 0.0))
                        
                        # Add each to purchase
                        price = round(random.uniform(10.0, 500.0), 2)
                        data.append((f"evt_{i}_p_{j}", session, user, ts, 'purchase', bp, price))
                    
        conn.executemany("""
            INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?)
        """, data)
        
        logger.info(f"Successfully inserted {len(data)} events.")

if __name__ == "__main__":
    seed_database()
