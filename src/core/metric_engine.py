import yaml
import os
import pandas as pd
from typing import Dict, Any
from src.db.db_client import DBClient
from src.utils.logger import get_logger
from src.utils.cache_manager import with_cache

logger = get_logger("metric_engine")

class MetricEngine:
    """MetricEngine — Orchestrates metric calculation using SQL models."""
    
    def __init__(self, db_client: DBClient, config_path: str = "config/metrics.yaml"):
        self.db = db_client
        with open(config_path, "r") as f:
            self.metrics_config = yaml.safe_load(f)
            
    @with_cache(ttl_seconds=300)
    def fetch_metric(self, metric_name: str) -> pd.DataFrame:
        """fetch_metric — Retrieves a metric's data by executing its associated SQL file."""
        if metric_name not in self.metrics_config:
            raise ValueError(f"Metric {metric_name} not found in config.")
            
        sql_file = self.metrics_config[metric_name]['sql_file']
        if not os.path.exists(sql_file):
            raise FileNotFoundError(f"SQL file {sql_file} for metric {metric_name} does not exist.")
            
        logger.info(f"Fetching metric: {metric_name}")
        return self.db.execute_file(sql_file)
        
    def get_all_metrics(self) -> Dict[str, pd.DataFrame]:
        """get_all_metrics — Computes all configured metrics."""
        results = {}
        for metric_name in self.metrics_config.keys():
            try:
                results[metric_name] = self.fetch_metric(metric_name)
            except Exception as e:
                logger.error(f"Failed to fetch {metric_name}: {e}")
        return results
