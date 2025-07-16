import pandas as pd
import json
from typing import Any, Dict
import numpy as np


class ReportBuilder:
    def __init__(self, output_path: str):
        self.output_path = output_path

    def write_json(self, results: Dict[str, Any]) -> None:
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)

    def write_csv(self, metrics: Dict[str, Any], interpretation: Dict[str, Any]) -> None:
        rows = []

        # Column-level metrics
        col_metrics = metrics.get("column_metrics", {})
        for column, metric_values in col_metrics.items():
            for metric, value in metric_values.items():
                rows.append({
                    "type": "column",
                    "column_or_group": column,
                    "metric": metric,
                    "value": self._normalize(value),
                    "risk": interpretation.get(column, {}).get("risk"),
                    "reason": interpretation.get(column, {}).get("reasons")
                })

        # Row-level metrics
        row_metrics = metrics.get("row_metrics", {})
        for metric_name, groupings in row_metrics.items():
            for group_key, values in groupings.items():
                for stat_name, value in values.items():
                    rows.append({
                        "type": "row",
                        "column_or_group": group_key,
                        "metric": f"{metric_name}:{stat_name}",
                        "value": self._normalize(value),
                        "risk": interpretation.get(f"{metric_name}:{group_key}", {}).get("risk"),
                        "reason": interpretation.get(f"{metric_name}:{group_key}", {}).get("reasons")
                    })

        df = pd.DataFrame(rows)
        df.to_csv(self.output_path, index=False)

    def _normalize(self, val: Any) -> Any:
        """Convert numpy types and nested values into flat, readable forms."""
        if isinstance(val, (np.floating, float)):
            return float(val)
        elif isinstance(val, (np.integer, int)):
            return int(val)
        elif isinstance(val, dict):
            return json.dumps({k: self._normalize(v) for k, v in val.items()})
        return val
