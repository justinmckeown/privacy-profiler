import pandas as pd
from pathlib import Path
from typing import List
from privacy_profiler.profiler.column_profile import ColumnProfiler
from privacy_profiler.metrics.column import GiniCoefficient, ShannonEntropyMetric, UniquenessRatioMetric, NullRatioMetric
from privacy_profiler.metrics.privacy_assessment_runner import PrivacyAssessmentRunner

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
        if not Path(path).exists():
            raise FileNotFoundError(f"Input file not found: {path or 'None'}")

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


    def run_profile(self, quasi_identifiers: List[str], sensitive_attributes: List[str] = None):
        if self.df is None:
            raise ValueError("No data loaded.")
        if not quasi_identifiers:
            raise ValueError("you must provide at least one quasi-identifier column")
        
        # TODO: Delete this line? I
        #column_metrics = self.profiler.profile(self.df)

        runner = PrivacyAssessmentRunner()
        assessment = runner.run(
            df=self.df,
            quasi_identifiers=quasi_identifiers,
            sensitive_attributes=sensitive_attributes
            )
        return assessment