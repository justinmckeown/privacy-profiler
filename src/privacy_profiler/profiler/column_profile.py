import pandas as pd
from typing import List, Dict
from privacy_profiler.metrics.base_metric import ColumnMetric

class ColumnProfiler:
    def __init__(self, metrics: List[ColumnMetric]):
        self.metrics = metrics

    def profile(self, df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """Return a dictionary of {column: {metric_name: score}}"""
        results = {}
        for col in df.columns:
            col_results = {}
            for metric in self.metrics:
                try:
                    col_results[metric.name()] = metric.compute(df[col])
                except Exception as e:
                    col_results[metric.name()] = None
            results[col] = col_results
        return results
