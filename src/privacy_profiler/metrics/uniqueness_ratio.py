import pandas as pd
from .base_metric import ColumnMetric

class UniquenessRatioMetric(ColumnMetric):
    def name(self) -> str:
        return "uniqueness_ratio"

    def compute(self, series: pd.Series) -> float:
        n_total = len(series)
        if n_total == 0:
            return 0.0
        n_unique = series.nunique(dropna=True)
        return round(n_unique / n_total, 4)
