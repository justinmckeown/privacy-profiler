import logging
from typing import List
from privacy_profiler.model.model import Model
from privacy_profiler.interface.rootview import RootViewController
from privacy_profiler.interpreter.interpretation_engine import InterpretationEngine



logger = logging.getLogger(__name__)

class Presenter:
    def __init__(self, model: Model, view: RootViewController, input_path: str, quasi_identifiers: List[str],  sensitive_attributes: List[str]):
        self.model = model
        self.view = view
        self.input_path = input_path
        self.quasi_identifiers = quasi_identifiers or []
        self.sensitive_attributes = sensitive_attributes or []
        self.interpreter = InterpretationEngine()


    def run(self) -> dict:
        self.view.display_intro()
        try:
            self.model.load_data(self.input_path)
        except ValueError as e:
            logging.error("Input file error: %s", str(e))
            self.view.display_error(f"Could not load input file: {e}")
            return {}
    
        try:
            results = self.model.run_profile(
                quasi_identifiers=self.quasi_identifiers,
                sensitive_attributes=self.sensitive_attributes
            )
    
            column_metrics = results.get("column_metrics", {})
            row_metrics = results.get("row_metrics", {})
            row_risk_summary = results.get("row_risk_summary", {})
    
            # Interpret both column-level and row-level metrics
            column_interpretation = self.interpreter.interpret_report(column_metrics)
            row_interpretation = self.interpreter.interpret_row_metrics(row_metrics)
    
            # Display combined output
            self.view.display_results(results, column_interpretation, row_risk_summary, row_interpretation)
    
            return {
                "metrics": results,
                "interpretation": {
                    "column": column_interpretation,
                    "row": row_interpretation
                },
                "row_risk_summary": row_risk_summary
            }
    
        except Exception as e:
            logging.exception("Unexpected error during profiling.")
            self.view.display_error(f"An error occurred: {e}")
            return {}
