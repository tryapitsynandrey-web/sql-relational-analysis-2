import os
import sys
import yaml

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils.logger import get_logger

logger = get_logger("generate_docs")

def generate_docs():
    """generate_docs — Parses YAML configuration and creates METRICS_DICTIONARY.md."""
    config_path = "config/metrics.yaml"
    output_path = "METRICS_DICTIONARY.md"
    
    logger.info(f"Reading configuration from {config_path}...")
    try:
        with open(config_path, "r") as f:
            metrics = yaml.safe_load(f)
            
        with open(output_path, "w") as f:
            f.write("# Metrics Dictionary\n\n")
            f.write("This document is auto-generated from `config/metrics.yaml`.\n\n")
            
            for name, details in metrics.items():
                f.write(f"## {name.replace('_', ' ').title()}\n")
                f.write(f"- **Domain**: {details.get('domain', 'N/A')}\n")
                f.write(f"- **Description**: {details.get('description', 'No description provided.')}\n")
                f.write(f"- **SQL File**: `{details.get('sql_file', 'unknown.sql')}`\n\n")
                
        logger.info(f"Successfully generated {output_path}.")
    except Exception as e:
        logger.error(f"Failed to generate documentation: {e}")

if __name__ == "__main__":
    generate_docs()
