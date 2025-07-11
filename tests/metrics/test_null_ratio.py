import pandas as pd
from privacy_profiler.metrics.null_ratio import NullRatioMetric

def test_null_ratio_half():
    series = pd.Series([None] * 50 + ['A'] * 50)
    ratio = NullRatioMetric().compute(series)
    assert abs(ratio - 0.5) < 0.01

def test_null_ratio_none():
    series = pd.Series(['A'] * 100)
    ratio = NullRatioMetric().compute(series)
    assert abs(ratio - 0.0) < 0.01
