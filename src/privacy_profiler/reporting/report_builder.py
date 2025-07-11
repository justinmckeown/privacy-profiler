import pandas as pd
import json
from typing import Any, Dict




class ReportBuilder:
    def __init__(self, output_path: str):
        self.output_path = output_path

    def write_json(self, results: Dict[str, Any]) -> None:
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)
    

    def write_csv(self, metrics: Dict[str, Dict[str, float]], interpretation: Dict[str, Dict[str, str]]) -> None:
        rows = []
        for column, metric_values in metrics.items():
            row = {"column": column, **metric_values, **interpretation.get(column, {})}
            rows.append(row)

        df = pd.DataFrame(rows)
        df.to_csv(self.output_path, index=False)


