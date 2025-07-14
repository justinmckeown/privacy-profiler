import json 
from privacy_profiler.model.model import Model


class RootViewController:
    def __init__(self, output_format: str = "text"):
        self.output_format = output_format

    def display_intro(self):
        print("Privacy Profiler: Starting analysis...\n")

    def display_results(
        self,
        metrics: dict,
        column_interpretation: dict,
        row_risk_summary: dict = None,
        row_interpretation: dict = None
    ):
        if self.output_format == "json":
            column_combined = {
                column: {
                    **metrics.get(column, {}),
                    **column_interpretation.get(column, {})
                }
                for column in metrics
            }

            output = {
                "column_metrics": column_combined,
                "row_metrics": row_risk_summary,
                "row_interpretation": row_interpretation or {}
            }

            print(json.dumps(output, indent=2))
            return

        # Plain text output
        for column in metrics:
            print(f"\n📊 Column: {column}")
            for k, v in metrics[column].items():
                print(f"  {k}: {v}")
            print(f"  Risk: {column_interpretation[column]['risk']}")
            print(f"  Reason(s): {column_interpretation[column]['reasons']}")

        if row_risk_summary:
            print("\n🔎 Row-Level Privacy Risk Summary")
            print("-----------------------------------")
            for k, v in row_risk_summary.items():
                print(f"{k.replace('_', ' ').capitalize()}: {v}")

        if row_interpretation:
            print("\n📘 Row-Level Metric Interpretations")
            print("-----------------------------------")
            for name, result in row_interpretation.items():
                print(f"{name}")
                print(f"  Risk: {result['risk']}")
                print(f"  Reason(s): {result['reasons']}")


    def display_error(self, message: str):
        print(f"[ERROR] {message}")
