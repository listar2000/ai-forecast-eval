# Forecasting ranking experiments

A small, extensible Python platform for comparing forecaster-ranking methods against known simulation truth. It supports paired Monte Carlo experiments, configuration files, three baseline methods, and reproducible result artifacts.

## Quick start

A local `.venv` has been prepared in this checkout. Run:

```bash
.venv/bin/forecast-eval configs/complete_overlap.yaml --output runs/my_first_run
.venv/bin/python -m pytest -q
```

For a fresh environment (Python 3.9 or newer):

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/python -m forecast_eval configs/random_missingness.yaml --output runs/random_run
```

Output paths must not already exist. The CLI returns 0 when every method produces a full ranking, 1 when a fit fails or a ranking is partial, and 2 for invalid CLI/configuration input. Tied ground truth can make a metric undefined even when a full ranking exists; this is not a fit failure.

## What is simulated

For event j, draw a true probability p_j uniformly from a configured interval. Forecaster i reports q_ij = p_j ± epsilon_i, with independent symmetric signs. Sample one Bernoulli outcome per event, shared across all forecasters. A separate participation mask determines which forecasts are visible to ranking methods. The optional market is another additive-error forecast for every event, with its own random stream.

The generator rejects error magnitudes that would put probabilities outside [0,1]; it does not clip forecasts. Uniform event probabilities can also be constant by using identical endpoints.

Ground-truth risk is the mean squared probability error over the **full common event set**, not over each model's observed subset. In this generator, it is epsilon_i squared. Expected Brier loss is p_j(1-p_j) + (q_ij-p_j)^2, so this oracle ranking also orders expected Brier losses on the common reference set. This is a specific estimand, not a universal definition of forecasting skill.

Methods receive an `ObservedForecasts` object containing IDs, masked forecasts, shared outcomes, and optional market forecasts. They do not receive true probabilities or hidden potential forecasts. Arrays are copied and read-only. Oracle data is retained separately for evaluation.

## Scenarios

| Config | Participation | Monte Carlo mode |
| --- | --- | --- |
| `configs/complete_overlap.yaml` | Every forecaster answers every event | Resample everything |
| `configs/random_missingness.yaml` | Independent observation probability 0.35 | Resample everything |
| `configs/staggered_participation.yaml` | Contiguous lifetimes spanning 60% of events | Resample everything |
| `configs/fixed_world.yaml` | Complete overlap | Hold probabilities, forecasts, market and mask fixed; resample outcomes |

Staggered entry follows the order of `epsilons`. The sample configuration puts the strongest forecaster first. Reverse the list to represent improving later entrants. Events are IID in all initial examples: temporal difficulty drift and strategic task selection are future mechanisms, not simulated implicitly.

The YAML files expose event count, probability range, forecaster errors, participation, market quality, seed, repetitions, methods, and metrics. Unknown keys and unsupported options are rejected. Repeat a method with different parameters by giving each entry a unique `label`.

## Included methods

- **Mean Brier:** negative average observed Brier loss.
- **Brier peer adjustment:** negative average of Brier loss minus the event's mean loss over observed forecasters, including self. Events with fewer than two participants are excluded. This deliberately simple baseline is not Metaculus's log-based Peer Score and does not solve shifting participant composition or disconnected comparison groups.
- **Market-relative Brier:** negative average loss difference against the market on the same observed events. Requires the complete market anchor. An imperfect market can introduce additional noise.

All returned scores are higher-is-better. Their numeric values are not assumed to share a skill scale. Under complete overlap all three methods differ only by a constant offset, so they must produce the same ranking.

## Metrics and failures

- **Pairwise accuracy:** proportion of correctly ordered pairs, excluding oracle ties. Estimated ties receive half credit.
- **Kendall tau-b:** tie-aware rank correlation. Undefined if either ordering has no variation.
- **Best selection:** probability of choosing a true best forecaster under uniform random tie-breaking among estimated winners.
- **Selection regret:** expected excess oracle risk under the same tie-breaking rule.
- **Estimate coverage** and **runtime:** fraction of forecasters with finite estimates and fit/result runtime in seconds.

Absolute score/risk differences of at most 1e-12 are treated as ties. Comparisons of numerical skill values and confidence-interval coverage are not implemented yet because the initial methods do not estimate a common calibrated skill parameter or intervals.

A forecaster with no usable data gets NaN internally, serialized as JSON `null`. If any forecaster is unranked, all ranking metrics for that method/replicate are null: the evaluator does not silently score an easier subpopulation. Failures are retained with error messages and zero estimate coverage. Aggregate metrics report valid counts, failure counts, and partial-ranking counts; valid-only averages must be read alongside those counts. Standard errors are undefined for fewer than two valid repetitions.

## Reproducibility and outputs

All methods share exactly the same data within each replicate. Separate deterministic random streams control event probabilities, forecast errors, participation, market forecasts, outcomes, and each method. Method seeds use stable labels, not Python's randomized hash. Changing method order or adding a method does not change existing methods' data or seeds. Extending the number of repetitions preserves earlier repetitions.

Each output directory contains:

- `config.json`: fully resolved configuration.
- `metadata.json`: package/dependency versions, Python/platform, Git state where available, and source-file SHA-256 hashes.
- `replicates.jsonl`: aligned scores, oracle risks, seeds, observation counts, diagnostics, statuses, and metrics.
- `summary.json`: method averages and Monte Carlo standard errors, plus paired method differences with their own standard errors.

Runtime and machine metadata vary between runs. Scientific outputs are deterministic for the same environment and configuration. Full forecast matrices are not stored by default; reconstruct a world using the saved resolved simulation configuration and `world_seed`, then use `outcome_seed` with NumPy's default generator. Artifacts contain oracle information for analysis; never supply it to a ranking method. `runs/` is Git-ignored. Nothing is committed automatically.

## Code map and extension

```text
src/forecast_eval/
  contracts.py         Shared observed-data, oracle, and result contracts
  simulation/          Validated components, world generation, outcomes, truth
  methods/             Base class, registry, and three vanilla methods
  evaluation/          Ranking metrics and ID-aligned oracle evaluation
  experiments/         Config loading, paired runner, aggregation, artifacts
  cli.py               Command-line entry point
configs/               Runnable examples
scripts/               Numerical validation beyond unit tests
tests/                Unit and integration tests
reading/               Research source collection
```

See [the extension guide](docs/extending.md) for adding a method or simulation mechanism, and [the validation report](docs/validation.md) for checks performed in this checkout.

Run the larger numerical validation independently:

```bash
.venv/bin/python scripts/validate_simulations.py --output runs/new_validation
```

Initial scope excludes fixed-effects regression, IRT fitting, uncertainty intervals, strategic reporting, adversarial selection, adaptive task allocation, and parallel execution. Those can be added without changing the observed-data/oracle separation. The runner currently retains result records in memory, so very large grids may eventually need streaming artifacts.
