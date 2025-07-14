import pandas as pd
from typing import List, Dict
from privacy_profiler.metrics.row.multi_column_metric import MultiColumnMetric

class RowProfiler:
    def __init__(self, metrics: List[MultiColumnMetric]):
        self.metrics = metrics

    def profile(
        self,
        df: pd.DataFrame,
        column_groups: Dict[str, List[str]]
    ) -> Dict[str, Dict[str, float]]:
        """
        Run all row-level metrics on specified column groups.

        Args:
            df: The dataset.
            column_groups: Dict where keys are labels (e.g. 'quasi_identifiers')
                           and values are lists of columns to pass to metrics.

        Returns:
            Dictionary of {metric_name: {group_name: result_dict}}
        """
        results = {}

        for metric in self.metrics:
            metric_name = metric.name()
            results[metric_name] = {}

            for group_label, columns in column_groups.items():
                try:
                    result = metric.compute(df, columns)
                    results[metric_name][group_label] = result
                except Exception as e:
                    results[metric_name][group_label] = {"error": str(e)}

        return results
