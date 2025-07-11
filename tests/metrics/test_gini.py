import pandas as pd
from privacy_profiler.metrics.gini import GiniCoefficient

def test_gini_uniform_distribution():
    series = pd.Series(['A', 'B', 'C', 'D'] * 25)
    gini = GiniCoefficient().compute(series)
    assert abs(gini - 0.0) < 0.01

def test_gini_skewed_distribution():
    series = pd.Series(['A'] * 90 + ['B'] * 10)
    gini = GiniCoefficient().compute(series)
    assert gini > 0.7
