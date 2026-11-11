# AI Forecast Eval

How reliably can we rank forecasters when they answer different questions? This project generates binary events and forecasters with known skill, gives each ranking method the same observed forecasts, and measures how often it recovers the true ordering. The initial baselines use mean Brier loss, peer adjustment, and market-relative scoring.

## Quick start

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run these commands from the repository root.

```bash
uv sync --locked
uv run forecast-eval configs/complete_overlap.yaml --output runs/first_run
uv run pytest -q
```

Open `runs/first_run/summary.json` for the ranking metrics and paired method comparisons. Choose a new output directory for each run.

## Repository layout

| Path | Purpose |
| --- | --- |
| [configs/](configs/) | Runnable scenarios for complete overlap, random missingness, staggered participation, and repeated outcomes in a fixed world |
| [simulation/](src/forecast_eval/simulation/) | Generate events, forecasts, participation masks, outcomes, and ground-truth skill |
| [methods/](src/forecast_eval/methods/) | Implement and register ranking methods using the shared [data and result types](src/forecast_eval/contracts.py) |
| [evaluation/](src/forecast_eval/evaluation/) | Compare estimated rankings with ground truth |
| [experiments/](src/forecast_eval/experiments/) | Run paired Monte Carlo repetitions and save results |
| [tests/](tests/) and [scripts/](scripts/) | Check implementation behavior and validate simulations against analytical expectations |
| [reading/](reading/README.md) | Papers and methodology references |

## Documentation

- [Running experiments, metrics, and output files](docs/experiments.md)
- [Adding a ranking method or simulation component](docs/extending.md)
- [Numerical validation results](docs/validation.md)
