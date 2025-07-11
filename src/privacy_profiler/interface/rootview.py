import json 
from privacy_profiler.model.model import Model


class RootViewController:
    def __init__(self, output_format:str = "text"):
        self.output_format = output_format

    def display_intro(self):
        print("Privacy Profiler: Starting analysis...\n")

    def display_results(self, metrics: dict, interpretations: dict, row_risk_summary: dict = None):
        if self.output_format == "json":
            combined = {
                column: {
                    **metrics.get(column, {}),
                    **interpretations.get(column, {})
                }
                for column in metrics
            }
            output = {
                "metrics": combined,
                "row_risk_summary": row_risk_summary
            }
            print(json.dumps(combined, indent=2))
        else:
            for column in metrics:
                print(f"\nColumn: {column}")
                for k, v in metrics[column].items():
                    print(f"  {k}: {v}")
                print(f"  Risk: {interpretations[column]['risk']}")
                print(f"  Reason(s): {interpretations[column]['reasons']}")
        
        if row_risk_summary:
            print("\n🔎 Row-Level Privacy Risk Summary")
            print("-----------------------------------")
            for k, v in row_risk_summary.items():
                print(f"{k.replace('_', ' ').capitalize()}: {v}")




    def display_error(self, message: str):
        print(f"[ERROR] {message}")
