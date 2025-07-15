import pandas as pd
from typing import List, Dict, Optional

from privacy_profiler.profiler.column_profile import ColumnProfiler
from privacy_profiler.profiler.row_profile import RowProfiler

from privacy_profiler.metrics.column import (
    GiniCoefficient,
    ShannonEntropyMetric,
    UniquenessRatioMetric,
    NullRatioMetric
)

from privacy_profiler.metrics.row import (
    KAnonymityMetric,
    LDiversityMetric,
    TClosenessMetric,
    MutualInformationMetric,
    MDLMetric
)


class PrivacyAssessmentRunner:
    def __init__(self):
        self.column_profiler = ColumnProfiler(metrics=[
            GiniCoefficient(),
            ShannonEntropyMetric(),
            UniquenessRatioMetric(),
            NullRatioMetric()
        ])
        self.row_profiler = RowProfiler(metrics=[
            KAnonymityMetric(),
            LDiversityMetric(),
            TClosenessMetric(),
            MutualInformationMetric(),
            MDLMetric()
        ])

    def run(self, df: pd.DataFrame, quasi_identifiers: List[str], sensitive_attributes: Optional[List[str]] = None) -> Dict[str, object]:
        if df.empty:
            raise ValueError("Provided DataFrame is empty.")

        if not quasi_identifiers:
            raise ValueError("You must provide at least one quasi-identifier.")

        row_columns = {}

        if sensitive_attributes:
            for attr in sensitive_attributes:
                row_columns[f"quasi_id_plus_{attr}"] = quasi_identifiers + [attr]

        else:
            row_columns = {
                "quasi_only": quasi_identifiers
            }

        # Column metrics
        column_results = self.column_profiler.profile(df)

        # Row metrics
        row_results = self.row_profiler.profile(df, row_columns)

        # Crude uniqueness risk summary (from RowRiskAssessor)
        unique_group_sizes = df.groupby(quasi_identifiers).size()
        unique_rows = (unique_group_sizes == 1).sum()
        percent_unique_rows = round(unique_rows / len(df) * 100, 2)

        if percent_unique_rows > 50:
            risk_level = "High"
        elif percent_unique_rows > 20:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        uniqueness_summary = {
            "quasi_identifiers": quasi_identifiers,
            "unique_row_count": int(unique_rows),
            "total_rows": len(df),
            "percent_unique_rows": percent_unique_rows,
            "row_risk_level": risk_level
        }

        return {
            "column_metrics": column_results,
            "row_metrics": row_results,
            "row_uniqueness_summary": uniqueness_summary
        }
