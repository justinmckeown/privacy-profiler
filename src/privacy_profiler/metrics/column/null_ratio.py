import pandas as pd
from .base_metric import ColumnMetric

class NullRatioMetric(ColumnMetric):
    def name(self) -> str:
        return "null_ratio"

    def compute(self, series: pd.Series) -> float:
        n_total = len(series)
        if n_total == 0:
            return 0.0
        n_nulls = series.isnull().sum()
        return round(n_nulls / n_total, 4)
