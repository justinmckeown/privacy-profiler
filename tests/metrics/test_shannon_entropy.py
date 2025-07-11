import pandas as pd
from privacy_profiler.metrics.shannon_entropy import ShannonEntropyMetric

def test_entropy_uniform_distribution():
    series = pd.Series(['A', 'B', 'C', 'D'] * 25)
    entropy = ShannonEntropyMetric().compute(series)
    assert abs(entropy - 2.0) < 0.1

def test_entropy_single_value():
    series = pd.Series(['A'] * 100)
    entropy = ShannonEntropyMetric().compute(series)
    assert abs(entropy - 0.0) < 0.01
