# Ranking methods

[base.py](base.py) defines `RankingMethod.fit(data)` and `result()`. [registry.py](registry.py) maps the names used in experiment YAML to method classes. The three baselines use [mean Brier loss](mean_brier.py), [loss relative to peers](peer_brier.py), or [loss relative to the market](market_relative_brier.py). They share the observed-loss averaging helper in [_utils.py](_utils.py).

**Add a method**

1. Create a module here and subclass `RankingMethod`. Accept `random_state` if you define a constructor. In `fit`, clear the previous result and compute scores from the supplied observations.
2. Store a `RankingResult` in `self._result` and return `self`. Include every forecaster ID, orient scores so higher is better, and return NaN for a forecaster whose score cannot be estimated.
3. Import the class in `registry.py` and add its YAML name to `METHODS`. Add an entry under `methods` in an experiment config, using `parameters` for constructor arguments. Check the scores on a small dataset with a known answer.

The [extension guide](../../../docs/extending.md) includes a class template and a configuration example for comparing two parameter settings.
