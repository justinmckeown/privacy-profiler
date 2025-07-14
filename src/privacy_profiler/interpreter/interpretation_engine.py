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

    
    def interpret_row_metrics(self, row_metrics: Dict[str, Dict[str, Dict[str, float]]]) -> Dict[str, Dict[str, str]]:
        interpreted = {}

        for metric, group_results in row_metrics.items():
            for group_label, values in group_results.items():
                reasons = []
                risk = "Low"

                if metric == "k_anonymity":
                    min_k = values.get("min_k", 99)
                    avg_k = values.get("avg_k", 0)
                    pct_violating = values.get("percent_classes_below_5", 0)

                    if min_k < 3:
                        risk = "High"
                        reasons.append(f"Minimum k is {min_k}")
                    elif pct_violating > 0.5:
                        risk = "Medium"
                        reasons.append(f"{int(pct_violating * 100)}% of equivalence classes violate k=5")

                    reasons.append(f"Average k: {avg_k}")

                elif metric == "l_diversity":
                    min_l = values.get("min_l", 99)
                    avg_l = values.get("avg_l", 0)
                    pct_violating = values.get("percent_classes_below_3", 0)

                    if min_l == 1:
                        risk = "High"
                        reasons.append("Minimum l is 1 (no diversity)")
                    elif pct_violating > 0.7:
                        risk = "Medium"
                        reasons.append(f"{int(pct_violating * 100)}% of classes have <3 distinct sensitive values")

                    reasons.append(f"Average l: {avg_l}")

                elif metric == "t_closeness":
                    max_t = values.get("max_t_distance", 0)
                    avg_t = values.get("avg_t_distance", 0)

                    if max_t > 0.3:
                        risk = "High"
                        reasons.append(f"Max t-distance is {max_t}")
                    elif avg_t > 0.15:
                        risk = "Medium"
                        reasons.append(f"Average t-distance is {avg_t}")

                    reasons.append(f"Avg t-distance: {avg_t}, Max: {max_t}")

                elif metric == "mutual_information":
                    mi = values.get("mutual_information_bits", 0)

                    if mi > 1.0:
                        risk = "High"
                        reasons.append(f"Mutual information is {mi} bits (strong predictability)")
                    elif mi > 0.5:
                        risk = "Medium"
                        reasons.append(f"Mutual information is {mi} bits (moderate linkage risk)")
                    else:
                        reasons.append(f"Mutual information is {mi} bits")

                elif metric == "minimum_description_length":
                    ratio = values.get("avg_compression_ratio", 0)

                    if ratio > 0.9:
                        risk = "Medium"
                        reasons.append(f"Average compression ratio is {ratio} (high information density)")
                    else:
                        reasons.append(f"Average compression ratio is {ratio}")

                interpreted[f"{metric}:{group_label}"] = {
                    "risk": risk,
                    "reasons": "; ".join(reasons)
                }

        return interpreted
    
    def interpret_report(self, report: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, str]]:
        """Interpret a full column-level metrics report."""
        return {
            col: self.interpret_column(col, metrics)
            for col, metrics in report.items()
        }