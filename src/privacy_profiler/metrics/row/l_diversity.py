import pandas as pd
from typing import List, Dict
from collections import Counter
from .multi_column_metric import MultiColumnMetric

class LDiversityMetric(MultiColumnMetric):
    def name(self) -> str:
        return "l_diversity"

    def compute(self, df: pd.DataFrame, columns: List[str]) -> Dict[str, float]:
        """
        Last item in `columns` is assumed to be the sensitive attribute.
        Others are quasi-identifiers.
        """
        if len(columns) < 2:
            raise ValueError("LDiversityMetric requires at least one QI and one sensitive attribute.")

        qi_columns = columns[:-1]
        sensitive_attr = columns[-1]

        equivalence_classes = df.groupby(qi_columns)[sensitive_attr]
        l_values = equivalence_classes.nunique()

        min_l = int(l_values.min())
        avg_l = float(l_values.mean())
        percent_below_l3 = (l_values < 3).sum() / len(l_values) if len(l_values) > 0 else 0

        return {
            "min_l": min_l,
            "avg_l": round(avg_l, 2),
            "percent_classes_below_3": round(percent_below_l3, 4)
        }
