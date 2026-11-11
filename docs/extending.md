# Extending the platform

## Add a ranking method

Subclass `RankingMethod`, accept constructor parameters and a `random_state`, clear fitted state at the start of each fit, and return a `RankingResult` with all forecaster IDs. Use NaN for models you cannot estimate. A thrown exception is recorded as a failed fit; other methods and repetitions still run.

```python
import numpy as np
from forecast_eval.contracts import RankingResult
from forecast_eval.methods.base import RankingMethod
from forecast_eval.methods.registry import register_method

class ExampleMethod(RankingMethod):
    def __init__(self, *, regularization=1.0, random_state=None):
        super().__init__(random_state=random_state)
        self.regularization = regularization
        # Validate your parameters here.

    def fit(self, data):
        self._result = None
        rng = np.random.default_rng(self.random_state)
        # Fit using data.forecasts, data.outcomes, and permitted auxiliaries.
        # Replace this illustrative placeholder with your actual estimator.
        scores = np.full(len(data.forecaster_ids), np.nan)
        self._result = RankingResult(
            data.forecaster_ids, scores,
            diagnostics={"regularization": self.regularization},
        )
        return self

register_method("example", ExampleMethod)
```

For CLI use, put the implementation under `methods/` and register it in `methods/registry.py`. Programmatic registrations must occur before configuration validation. Third-party entry-point discovery is not implemented.

Configure independent variants using labels:

```yaml
methods:
  - name: example
    label: example_regularized
    parameters:
      regularization: 1.0
  - name: example
    label: example_unregularized
    parameters:
      regularization: 0.0
```

Labels determine stable per-method random seeds. Scores must be oriented higher-is-better; return negative losses if appropriate. Result ID order may differ from input order; the evaluator aligns IDs before grading. Diagnostics should contain JSON-compatible values or NumPy arrays/scalars. Do not read simulation files or oracle data inside a method. If you want interval evaluation, first define a shared target/scale and extend the result contract and evaluator explicitly.

## Add a simulation component

The components are intentionally small, typed functions rather than an inheritance framework:

1. Add validated fields/options in `simulation/config.py`.
2. Implement the corresponding generator in `events.py`, `forecasters.py`, or `participation.py` and dispatch on its configured name.
3. Keep random state explicit. Reuse that component's existing independent stream, or append a new stream without renumbering the existing streams in `generate_world`.
4. Preserve a full potential forecast matrix before masking. Recompute oracle risk from actual probabilities/forecasts, rather than assuming it equals epsilon squared.
5. Add analytic or controlled fixtures for the new behavior and a runnable YAML scenario.

Currently `generate_mask` takes shape, configuration, and RNG. A selective-participation mechanism will need an explicit context argument describing what the selection policy can see (for example probabilities, domains, or a forecaster's private information). That context belongs to simulation and is never automatically exposed to ranking methods. Document the information assumptions for any adversarial policy.

For logit errors, clipping, heteroskedastic forecasters, or domain-specific strengths, the current `compute_truth` still computes finite-reference squared probability risk correctly. For other estimands, implement an explicit truth option and document its relationship to the evaluation goal.

## Reconstruct one saved replicate

```python
import json
import numpy as np
from pathlib import Path
from forecast_eval.experiments.config import config_from_dict
from forecast_eval.simulation.generate import generate_world

run = Path("runs/complete_overlap")
config = config_from_dict(json.loads((run / "config.json").read_text()))
record = json.loads((run / "replicates.jsonl").read_text().splitlines()[0])
world = generate_world(config.simulation, record["world_seed"])
data = world.observe(np.random.default_rng(np.random.SeedSequence(record["outcome_seed"])))
```

Use the same package/dependency versions recorded in `metadata.json`. The files record source hashes to identify the implementation; they do not archive executable source by themselves.
