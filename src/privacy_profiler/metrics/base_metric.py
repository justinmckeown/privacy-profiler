from abc import ABC, abstractmethod
import pandas as pd

class ColumnMetric(ABC):
    """Abstract base class for all column-level metrics."""

    @abstractmethod
    def compute(self, series: pd.Series) -> float:
        """Compute the metric on a pandas Series."""
        pass

    @abstractmethod
    def name(self) -> str:
        """Return the name of the metric."""
        pass
