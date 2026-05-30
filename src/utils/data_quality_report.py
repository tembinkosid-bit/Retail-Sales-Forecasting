import json
import pandas as pd


class DataQualityReport:
    def __init__(self):
        self.report = {}

    def add_file_stats(self, file_name, df_before: pd.DataFrame, df_after: pd.DataFrame = None):

        self.report[file_name] = {
            "rows_before": len(df_before),
            "columns": len(df_before.columns),
            "null_ratio_avg": float(df_before.isnull().mean().mean()),
            "duplicate_ratio": float(df_before.duplicated().mean())
        }

        if df_after is not None:
            self.report[file_name]["rows_after"] = len(df_after)
            self.report[file_name]["rows_removed"] = len(df_before) - len(df_after)

    def to_dataframe(self) -> pd.DataFrame:
        """
        SINGLE SOURCE OF TRUTH CONVERSION
        """
        rows = []

        for file_name, metrics in self.report.items():
            for metric, value in metrics.items():
                rows.append({
                    "file_name": file_name,
                    "metric": metric,
                    "value": value
                })

        return pd.DataFrame(rows)

    def save(self, output_path="data_quality_report.json"):
        with open(output_path, "w") as f:
            json.dump(self.report, f, indent=4, default=str)