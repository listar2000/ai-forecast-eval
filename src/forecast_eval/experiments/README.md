# Experiments

| File | Responsibility |
| --- | --- |
| [config.py](config.py) | Load YAML and validate scenario, method, and metric selections |
| [runner.py](runner.py) and [monte_carlo.py](monte_carlo.py) | Generate each replicate, assign reproducible seeds, and fit every method on shared observations |
| [summarize.py](summarize.py) | Compute method averages, paired differences, and Monte Carlo standard errors |
| [artifacts.py](artifacts.py) | Save the resolved config, per-replicate records, summary, and software versions |

**Add an experiment.** From the repository root, copy an existing scenario and edit its event count, coverage, methods, or number of replicates. Use `resample_world` to draw a new environment each time or `fixed_world` to hold forecasts and participation fixed while resampling outcomes.

```bash
cp configs/random_missingness.yaml configs/my_experiment.yaml
# Edit configs/my_experiment.yaml, then run:
uv run forecast-eval configs/my_experiment.yaml --output runs/my_experiment
```

Choose a fresh output directory. Read `summary.json` for the comparison and `replicates.jsonl` to inspect individual fits. See the [experiment guide](../../../docs/experiments.md) for metric definitions and output fields.
