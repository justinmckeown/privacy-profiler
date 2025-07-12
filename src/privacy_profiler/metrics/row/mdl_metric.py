import pandas as pd
import zlib
from typing import List, Dict
from .multi_column_metric import MultiColumnMetric

class MDLMetric(MultiColumnMetric):
    def name(self) -> str:
        return "minimum_description_length"

    def compute(self, df: pd.DataFrame, columns: List[str]) -> Dict[str, float]:
        """
        Computes a compression ratio for each column and returns the average.

        Lower ratio → more compressible → lower uniqueness/information density.
        """
        if not columns:
            raise ValueError("MDLMetric requires at least one column.")

        compression_ratios = {}

        for col in columns:
            series = df[col].astype(str).fillna("NA")
            raw = '|'.join(series.tolist()).encode('utf-8')
            original_size = len(raw)
            compressed_size = len(zlib.compress(raw))
            ratio = compressed_size / original_size if original_size > 0 else 1.0
            compression_ratios[col] = round(ratio, 4)

        avg_ratio = round(sum(compression_ratios.values()) / len(compression_ratios), 4)

        result = {"avg_compression_ratio": avg_ratio}
        result.update({f"ratio_{col}": val for col, val in compression_ratios.items()})

        # TODO: Consider using other compression methods or modeling MDL more formally

        return result
