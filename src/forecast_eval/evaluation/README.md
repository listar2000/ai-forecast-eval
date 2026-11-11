# Evaluation

[evaluate.py](evaluate.py) aligns scores and oracle risks by forecaster ID and reports the fraction of forecasters with a finite estimate. [ranking.py](ranking.py) computes pairwise accuracy, Kendall’s tau-b, best-forecaster selection, and selection regret. Higher scores indicate better estimated skill. Lower oracle risk indicates better true skill.

**Add a ranking metric**

1. Add its configuration name to `METRICS` in `ranking.py` and return its value under that name from `ranking_metrics`. Specify how ties affect the value and when it is undefined. The existing partial-ranking path returns `None` for every registered metric.
2. Check a hand-calculated ranking, including a tie or a missing estimate. See the [metric tests](../../../tests/test_methods_metrics.py).
3. Include the name in a YAML config’s `metrics` list. The runner records the value for each replicate and summarizes it across repetitions. Document its interpretation in the [experiment guide](../../../docs/experiments.md).
