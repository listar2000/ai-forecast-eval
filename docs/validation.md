# Validation report

Executed November 9, 2026 in the project-local virtual environment. No commits were made.

## Automated checks

- 31 unit/integration tests passed (`python -m pytest -q`).
- Tests include the Brier decomposition, epsilon-squared oracle risk, shared outcomes, isolated random streams, mask invariance, hand-calculated baseline scores, missing histories, ties, ID alignment, fit failures, stochastic-method seeds, method reordering, repeat extension, artifact writing, and CLI errors.
- Kendall tau-b checked against SciPy on 50 independently generated tie-containing vectors.
- `pip check` passed and all Python source, scripts, and tests compiled.
- A second CLI process reproduced all 600 scientific records from the complete-overlap run exactly after excluding runtime.

## End-to-end example scenarios

Each scenario used 200 paired repetitions with 1,000 events and all three methods. All 2,400 fits across these four scenarios returned complete estimates without failures.

| Scenario | Mean Brier pairwise accuracy | Brier peer accuracy | Market-relative accuracy |
| --- | ---: | ---: | ---: |
| complete_overlap | 0.9615 | 0.9615 | 0.9615 |
| random_missingness | 0.7925 | 0.8390 | 0.8185 |
| staggered_participation | 0.8750 | 0.7870 | 0.8895 |
| fixed_world | 0.9560 | 0.9560 | 0.9560 |

With complete overlap, all ranking metrics agree exactly between all methods. This is expected because their scores differ by a constant shared offset. Under staggered participation, simple peer adjustment performs worse in this particular scenario; it is a baseline failure mode, not a software error or a claim of universal inferiority.

## Numerical validation beyond unit tests

The reproducible script is `scripts/validate_simulations.py`; final artifacts are in `runs/numerical_validation_final/`.

Three sample-size experiments used 300 paired repetitions each:

| Events | Pairwise accuracy | Best selection | Selection regret |
| --- | ---: | ---: | ---: |
| 100 | 0.787667 | 0.333333 | 0.00325625 |
| 1000 | 0.963667 | 0.800000 | 0.00025000 |
| 10000 | 0.999667 | 0.996667 | 0.00000208 |

These are the Mean Brier results; all three methods give identical rankings with complete overlap. Saved summaries include Monte Carlo standard errors.

For a separate fixed world, 2,000 outcome samples checked empirical Brier-loss gaps against analytical epsilon-squared gaps:

| Epsilon | Analytical gap | Empirical gap | Monte Carlo SE |
| --- | ---: | ---: | ---: |
| 0 | 0.00000000 | 0.00000000 | 0.00000000 |
| 0.025 | 0.00062500 | 0.00063010 | 0.00001656 |
| 0.05 | 0.00250000 | 0.00247292 | 0.00003326 |
| 0.1 | 0.01000000 | 0.01002251 | 0.00006732 |
| 0.15 | 0.02250000 | 0.02258107 | 0.00009811 |

All deviations are within the predeclared six-MCSE tolerance (in this run, each nonzero deviation was also below one MCSE). This checks expected score behavior, not the strategic optimality of truthful reporting in a competition.

Additional runs checked zero observed forecasts and equal oracle skills. Empty histories produce partial results, zero coverage, and null ranking metrics rather than fabricated scores. Equal skills give no pairwise target ordering, full best-selection credit, and effectively zero regret.

## Limits

These checks support correctness of the implemented initial family; they are not proof of correctness for every future extension. The present model uses binary independent events, additive fixed-magnitude errors, a stationary optional market, and uniform common-reference risk. It does not yet model strategic reporting, selective participation, temporal difficulty drift, or fit uncertainty. Results from incomplete/failed rankings are not silently included in ranking averages; inspect valid counts. Runtime is intentionally excluded from exact reproducibility comparisons.
