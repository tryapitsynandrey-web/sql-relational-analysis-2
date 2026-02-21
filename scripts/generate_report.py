import os
import sys

# Ensure src in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db.db_client import DBClient
from src.core.metric_engine import MetricEngine
from src.utils.export_manager import ExportManager
from src.utils.logger import get_logger

logger = get_logger("generate_report")

def run_export():
    """run_export — Uses the metric engine to fetch data and export it via ExportManager."""
    logger.info("Initializing Export Process...")
    
    db_client = DBClient()
    engine = MetricEngine(db_client)
    exporter = ExportManager()
    
    results = {}
    
    for metric_name in engine.metrics_config.keys():
        logger.info(f"Exporting {metric_name}...")
        try:
            df = engine.fetch_metric(metric_name)
            exporter.export_csv(df, metric_name)
            exporter.export_json(df, metric_name)
            results[metric_name] = df
        except Exception as e:
            logger.error(f"Failed to export {metric_name}: {e}")
            
    exporter.export_summary_md(results)
    logger.info("Export Complete! Check the exports/ directory.")

if __name__ == "__main__":
    run_export()
