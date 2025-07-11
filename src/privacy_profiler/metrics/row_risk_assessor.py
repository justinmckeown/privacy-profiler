import pandas as pd
from typing import List, Dict

class RowRiskAssessor:
    def __init__(self, quasi_identifiers: List[str]):
        self.quasi_identifiers = quasi_identifiers

    def assess(self, df: pd.DataFrame) -> Dict[str, object]:
        if not self.quasi_identifiers:
            raise ValueError("Quasi-identifiers must be specified for row risk assessment.")

        grouped = df.groupby(self.quasi_identifiers)
        group_sizes = grouped.size()
        unique_rows = (group_sizes == 1).sum()
        total_rows = len(df)
        percent_unique = round((unique_rows / total_rows) * 100, 2)

        if percent_unique > 50:
            risk_level = "High"
        elif percent_unique > 20:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        return {
            "quasi_identifiers": self.quasi_identifiers,
            "unique_row_count": int(unique_rows),
            "total_rows": total_rows,
            "percent_unique_rows": percent_unique,
            "row_risk_level": risk_level
        }
