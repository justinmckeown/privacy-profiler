import numpy as np
import pandas as pd
from .base_metric import ColumnMetric

class GiniCoefficient(ColumnMetric):
    def name(self) -> str:
        return "gini_coefficient"

    def compute(self, series: pd.Series) -> float:
        counts = series.value_counts().values
        if len(counts) == 0:
            return 0.0

        sorted_counts = np.sort(counts)
        n = len(sorted_counts)
        cumvals = np.cumsum(sorted_counts)
        gini = (2 * np.sum((np.arange(1, n+1) * sorted_counts)) / (n * cumvals[-1])) - (n + 1) / n
        return round(gini, 4)
