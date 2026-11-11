"""Numerical validation beyond unit tests; writes reproducible evidence to runs/.

Run: python scripts/validate_simulations.py --output runs/numerical_validation
Statistical assertions use broad, predeclared tolerances, not rounded rankings.
"""
import argparse
import json
from dataclasses import replace
from pathlib import Path
import numpy as np
from forecast_eval.experiments.config import load_config
from forecast_eval.experiments.runner import run_experiment
from forecast_eval.experiments.artifacts import write_artifacts, dumps
from forecast_eval.simulation.config import ParticipationConfig, ForecasterConfig
from forecast_eval.simulation.generate import generate_world
from forecast_eval.experiments.monte_carlo import outcome_rng


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    base = replace(load_config('configs/complete_overlap.yaml'), replicates=300)
    checks = {}
    curve = []
    for count in [100, 1000, 10000]:
        cfg = replace(base, simulation=replace(base.simulation, events=replace(base.simulation.events, count=count)))
        rows, summary = run_experiment(cfg)
        assert all(r['status'] == 'ok' for r in rows)
        for pair in summary['paired_differences']:
            assert all(m['mean'] == 0 for m in pair['metrics'].values())
        write_artifacts(args.output/f'events_{count}', cfg, rows, summary)
        metrics = summary['methods']['mean_brier']['metrics']
        curve.append({'events': count, 'pairwise_accuracy': metrics['pairwise_accuracy'],
                      'best_selection': metrics['best_selection'], 'selection_regret': metrics['selection_regret']})
    assert curve[-1]['pairwise_accuracy']['mean'] > curve[0]['pairwise_accuracy']['mean'] + 0.05
    assert curve[-1]['selection_regret']['mean'] < curve[0]['selection_regret']['mean']
    checks['sample_size_curve'] = curve
    checks['complete_overlap_rankings_identical'] = True

    # Isolate outcome noise in one world and compare empirical LOSS DIFFERENCES
    # to epsilon^2 differences. Per-replicate differences preserve shared outcomes.
    world = generate_world(base.simulation, [932, 0, 0])
    q, p = world.truth.potential_forecasts, world.truth.probabilities
    differences = []
    for replicate in range(2000):
        y = world.observe(outcome_rng(932, replicate)).outcomes
        loss = ((q-y) ** 2).mean(axis=1)
        differences.append(loss-loss[0])
    values = np.array(differences)
    empirical = values.mean(axis=0)
    expected = world.truth.risks-world.truth.risks[0]
    mcse = values.std(axis=0, ddof=1)/np.sqrt(len(values))
    assert np.all(np.abs(empirical-expected) <= 6*mcse + 1e-12)
    checks['expected_brier_gaps'] = {'replicates': len(values), 'empirical': empirical,
                                    'analytical': expected, 'mcse': mcse, 'within_six_mcse': True}

    # No observation is silently turned into a zero loss or a successful ranking.
    empty = replace(base, replicates=3, simulation=replace(base.simulation,
        participation=ParticipationConfig('random', observation_probability=0)))
    rows, summary = run_experiment(empty)
    assert all(r['status'] == 'partial' and r['metrics']['estimate_coverage'] == 0 for r in rows)
    assert all(r['metrics']['pairwise_accuracy'] is None for r in rows)
    write_artifacts(args.output/'empty_histories', empty, rows, summary)
    checks['empty_histories_explicitly_unranked'] = True

    equal = replace(base, replicates=10, simulation=replace(base.simulation,
        forecasters=ForecasterConfig(epsilons=(0.05,0.05,0.05))))
    rows, summary = run_experiment(equal)
    assert all(r['metrics']['best_selection'] == 1 for r in rows)
    assert all(r['metrics']['pairwise_accuracy'] is None for r in rows)
    assert all(r['metrics']['selection_regret'] < 1e-12 for r in rows)
    write_artifacts(args.output/'equal_skills', equal, rows, summary)
    checks['true_skill_ties_handled'] = True
    (args.output/'checks.json').write_text(dumps(checks)+'\n')
    print(json.dumps(json.loads(dumps(checks)), indent=2))


if __name__ == '__main__':
    main()
