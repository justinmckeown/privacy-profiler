from abc import ABC, abstractmethod
import pandas as pd
from typing import List, Dict

class MultiColumnMetric(ABC):
    """Abstract base class for metrics operating on multiple columns."""

    @abstractmethod
    def name(self) -> str:
        """Return the name of the metric."""
        pass

    @abstractmethod
    def compute(self, df: pd.DataFrame, columns: List[str]) -> Dict[str, float]:
        """Compute the metric on the specified columns of a DataFrame.

        Args:
            df: The dataset.
            columns: List of column names to compute the metric on.

        Returns:
            Dictionary of results relevant to the metric.
        """
        pass
