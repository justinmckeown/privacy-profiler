import pandas as pd
from pathlib import Path
from privacy_profiler.profiler.column_profile import ColumnProfiler
from privacy_profiler.metrics import GiniCoefficient, ShannonEntropyMetric, UniquenessRatioMetric, NullRatioMetric, RowRiskAssessor

class Model:
    def __init__(self):
        self.df = None
        self.profiler = ColumnProfiler(metrics=[
            GiniCoefficient(),
            ShannonEntropyMetric(), 
            UniquenessRatioMetric(),
            NullRatioMetric()
            # NOTE: add other metrics here
        ])

    def load_data(self, path: str) -> None:
        ext = Path(path).suffix.lower()
        if ext == ".csv":
            self.df = pd.read_csv(path)
        elif ext == ".parquet":
            self.df = pd.read_parquet(path)
        elif ext in [".xls", ".xlsx"]:
            self.df = pd.read_excel(path)
        elif ext == ".json":
            self.df = pd.read_json(path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")


    def run_profile(self):
        if self.df is None:
            raise ValueError("No data loaded.")
        

        column_metrics = self.profiler.profile(self.df)

        # TODO: Make this configurable later; for now it's hardcoded
        quasi_identifiers = ["email", "postcode"]
        row_risk = RowRiskAssessor(quasi_identifiers).assess(self.df)

        return {
            "metrics": column_metrics,
            "row_risk_summary": row_risk
        }