import pandas as pd
from privacy_profiler.metrics.uniqueness_ratio import UniquenessRatioMetric

def test_uniqueness_full():
    series = pd.Series([str(i) for i in range(100)])
    ratio = UniquenessRatioMetric().compute(series)
    assert abs(ratio - 1.0) < 0.01

def test_uniqueness_none():
    series = pd.Series(['A'] * 100)
    ratio = UniquenessRatioMetric().compute(series)
    assert abs(ratio - 0.01) < 0.01  # Only one unique value
