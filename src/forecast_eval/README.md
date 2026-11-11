# Forecast evaluation package

Each Monte Carlo replicate creates one forecasting dataset. Every method sees the same observed forecasts and outcomes. The evaluator compares each fitted ranking with the known risk of each forecaster across the full event set.

| Module | Role |
| --- | --- |
| [simulation](simulation/README.md) | Generate events, forecasts, outcomes, participation, and ground truth |
| [methods](methods/README.md) | Fit ranking methods to observed forecasts |
| [evaluation](evaluation/README.md) | Measure how well the estimated ordering recovers ground truth |
| [experiments](experiments/README.md) | Run paired repetitions, compare methods, and write results |

[contracts.py](contracts.py) defines the three objects passed between modules. Methods receive `ObservedForecasts` and return a `RankingResult`. The evaluator also receives `SimulationTruth`.

To run a new comparison, start with a YAML file in [configs](../../configs/). The `forecast-eval` command loads it through [cli.py](cli.py). Running `python -m forecast_eval` uses the same entry point through [__main__.py](__main__.py).
