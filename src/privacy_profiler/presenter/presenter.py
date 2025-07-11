import logging
from privacy_profiler.model.model import Model
from privacy_profiler.interface.rootview import RootViewController
from privacy_profiler.interpreter.interpretation_engine import InterpretationEngine



logger = logging.getLogger(__name__)

class Presenter:
    def __init__(self, model: Model, view: RootViewController, input_path: str):
        self.model = model
        self.view = view
        self.input_path = input_path
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
            results = self.model.run_profile()
            metrics = results["metrics"]
            row_risk = results.get("row_risk_summary", {})

            interpretations = self.interpreter.interpret_report(metrics)
            self.view.display_results(results, interpretations, row_risk)
            return {
                "metrics": results,
                "interpretation": interpretations,
                "row_risk_summary": row_risk
            }
        except Exception as e:
            logging.exception("Unexpected error during profiling.")
            self.view.display_error(f"An error occurred: {e}")
            return {}