import pandas as pd
from typing import List, Dict
from .multi_column_metric import MultiColumnMetric

class KAnonymityMetric(MultiColumnMetric):
    def name(self) -> str:
        return "k_anonymity"

    def compute(self, df: pd.DataFrame, columns: List[str]) -> Dict[str, float]:
        if not columns:
            raise ValueError("At least one quasi-identifier column must be specified.")

        # Group by quasi-identifiers
        equivalence_counts = df.groupby(columns).size()

        min_k = equivalence_counts.min()
        avg_k = equivalence_counts.mean()
        percent_violating_k5 = (equivalence_counts < 5).sum() / len(equivalence_counts)

        return {
            "min_k": int(min_k),
            "avg_k": round(avg_k, 2),
            "percent_classes_below_5": round(percent_violating_k5, 4)
        }
