import pandas as pd
import json
import os
from datetime import datetime

class ExportManager:
    """ExportManager — Universal exporter converting metric logic out to CSV, JSON, MD."""
    
    def __init__(self, export_dir: str = "exports/"):
        self.export_dir = export_dir
        os.makedirs(self.export_dir, exist_ok=True)
        
    def export_csv(self, df: pd.DataFrame, metric_name: str) -> str:
        """export_csv — Dumps dataframe to a CSV file."""
        if df is None or df.empty:
            return ""
        path = os.path.join(self.export_dir, f"{metric_name}.csv")
        df.to_csv(path, index=False)
        return path
        
    def export_json(self, df: pd.DataFrame, metric_name: str) -> str:
        """export_json — Dumps dataframe to JSON format."""
        if df is None or df.empty:
            return ""
        path = os.path.join(self.export_dir, f"{metric_name}.json")
        df.to_json(path, orient="records", indent=2)
        return path
        
    def export_summary_md(self, reports_data: dict) -> str:
        """export_summary_md — Builds a detailed markdown summary for the overall reports."""
        path = os.path.join(self.export_dir, "summary_report.md")
        with open(path, "w") as f:
            f.write("# Automated Summary Report\n")
            f.write(f"Generated at: {datetime.now().isoformat()}\n\n")
            for metric, data in reports_data.items():
                f.write(f"## {metric}\n")
                if isinstance(data, pd.DataFrame) and not data.empty:
                    f.write(data.head(5).to_markdown(index=False))
                else:
                    f.write(str(data))
                f.write("\n\n")
        return path
