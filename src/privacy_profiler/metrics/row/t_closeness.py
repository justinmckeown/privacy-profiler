import pandas as pd
from typing import List, Dict
from .multi_column_metric import MultiColumnMetric

class TClosenessMetric(MultiColumnMetric):
    def name(self) -> str:
        return "t_closeness"

    def compute(self, df: pd.DataFrame, columns: List[str]) -> Dict[str, float]:
        """
        Last item in `columns` is the sensitive attribute.
        Others are quasi-identifiers.

        Computes t-closeness using Total Variation Distance (TVD).
        """
        if len(columns) < 2:
            raise ValueError("TClosenessMetric requires at least one QI and one sensitive attribute.")

        qi_columns = columns[:-1]
        sensitive_attr = columns[-1]

        # Overall distribution of sensitive attribute
        global_dist = df[sensitive_attr].value_counts(normalize=True)

        distances = []
        grouped = df.groupby(qi_columns)

        for _, group in grouped:
            class_dist = group[sensitive_attr].value_counts(normalize=True)
            aligned = global_dist.align(class_dist, fill_value=0)

            # Total Variation Distance (symmetric, bounded)
            diff = (aligned[0] - aligned[1]).abs().sum() / 2
            distances.append(diff)

        if not distances:
            return {"avg_t_distance": 0.0, "max_t_distance": 0.0}

        avg_t = round(sum(distances) / len(distances), 4)
        max_t = round(max(distances), 4)

        return {
            "avg_t_distance": avg_t,
            "max_t_distance": max_t
        }

        # TODO: Add optional support for KL-divergence and Earth Mover's Distance (EMD)
        # for better support of numeric or ordinal sensitive attributes.

        # NOTE: TVD (current appraoch) - Measures the maximum difference between two probability distributions. Symmetric, bounded, and intuitive. Faster at scale, and gives approximate KL. 
        # NOTE: EMD - Measures the “effort” to turn one distribution into another. Best for ordinal or continuous sensitive attributes. Sensitive attribute is ordinal or numeric
        # NOTE: KL-divergence - Measures information gain/loss from using one distribution to approximate another. Asymmetric, unbounded, and sensitive to zero-probability bins. Want an information-theoretic interpretation
