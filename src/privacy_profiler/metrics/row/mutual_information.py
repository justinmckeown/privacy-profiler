import pandas as pd
from typing import List, Dict
from sklearn.metrics import mutual_info_score
from .multi_column_metric import MultiColumnMetric

class MutualInformationMetric(MultiColumnMetric):
    def name(self) -> str:
        return "mutual_information"

    def compute(self, df: pd.DataFrame, columns: List[str]) -> Dict[str, float]:
        """
        Last column is treated as the sensitive attribute.
        Others are quasi-identifiers.
        """
        if len(columns) < 2:
            raise ValueError("MutualInformationMetric requires at least one QI and one sensitive attribute.")

        qi_columns = columns[:-1]
        sensitive_attr = columns[-1]

        # Join QIs into a single composite string
        qi_values = df[qi_columns].astype(str).agg('|'.join, axis=1)
        sensitive_values = df[sensitive_attr].astype(str)

        mi = mutual_info_score(qi_values, sensitive_values)

        return {
            "mutual_information_bits": round(mi, 4)
        }

        # TODO: Add support for normalized or conditional MI if needed
