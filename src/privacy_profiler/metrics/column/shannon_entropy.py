import pandas as pd
import numpy as np
from .base_metric import ColumnMetric

class ShannonEntropyMetric(ColumnMetric):
    def name(self) -> str:
        return "shannon_entropy"

    def compute(self, series: pd.Series) -> float:
        counts = series.value_counts(dropna=True)
        probabilities = counts / counts.sum()

        entropy = -np.sum(probabilities * np.log2(probabilities))
        return round(entropy, 4)
