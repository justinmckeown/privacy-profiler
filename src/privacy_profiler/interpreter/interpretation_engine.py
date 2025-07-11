from typing import Dict

class InterpretationEngine:
    def interpret_column(self, column_name: str, metrics: Dict[str, float]) -> Dict[str, str]:
        risk = "Low"
        reasons = []

        if metrics.get("uniqueness_ratio", 0) > 0.8:
            risk = "High"
            reasons.append("High uniqueness ratio")

        if metrics.get("shannon_entropy", 0) < 1.0:
            reasons.append("Low entropy")

        if metrics.get("gini_coefficient", 0) > 0.6:
            reasons.append("Skewed distribution (high Gini)")

        return {
            "risk": risk,
            "reasons": "; ".join(reasons) or "No significant risk indicators"
        }

    def interpret_report(self, report: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, str]]:
        return {
            col: self.interpret_column(col, metrics)
            for col, metrics in report.items()
        }
