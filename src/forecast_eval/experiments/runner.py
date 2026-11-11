import time
import numpy as np
from .monte_carlo import method_seed, outcome_rng
from .summarize import summarize
from ..simulation.generate import generate_world
from ..methods.registry import make_method
from ..evaluation.evaluate import evaluate


def run_experiment(config, progress=None):
    """Paired repetitions; retains small result records, not full datasets."""
    records = []
    fixed = generate_world(config.simulation, [config.seed, 0, 0]) if config.mode == 'fixed_world' else None
    for replicate in range(config.replicates):
        world_seed = [config.seed, 0, 0 if fixed is not None else replicate]
        world = fixed if fixed is not None else generate_world(config.simulation, world_seed)
        data = world.observe(outcome_rng(config.seed, replicate))
        for spec in config.methods:
            seed = method_seed(config.seed, replicate, spec.key)
            record = {'replicate': replicate, 'method': spec.key, 'method_name': spec.name,
                      'world_seed': world_seed, 'outcome_seed': [config.seed, 1, replicate],
                      'method_seed': seed, 'forecaster_ids': list(world.truth.forecaster_ids),
                      'oracle_risks': world.truth.risks.tolist(), 'scores': None, 'diagnostics': {},
                      'observed_counts': np.isfinite(data.forecasts).sum(axis=1).tolist(),
                      'status': 'ok', 'error': None}
            start = time.perf_counter()
            try:
                method = make_method(spec.name, spec.parameters, seed)
                result = method.fit(data).result()
                elapsed = time.perf_counter() - start
                all_metrics = evaluate(result, world.truth)
                record['metrics'] = {m: all_metrics[m] for m in config.metrics}
                record['metrics']['estimate_coverage'] = all_metrics['estimate_coverage']
                scores_by_id = dict(zip(result.forecaster_ids, result.scores))
                record['scores'] = [scores_by_id[i] for i in world.truth.forecaster_ids]
                record['diagnostics'] = dict(result.diagnostics)
                if all_metrics['estimate_coverage'] < 1:
                    record['status'] = 'partial'
            except Exception as exc:
                elapsed = time.perf_counter() - start
                record['status'] = 'failed'
                record['error'] = f'{type(exc).__name__}: {exc}'
                record['metrics'] = {m: None for m in config.metrics}
                record['metrics']['estimate_coverage'] = 0.0
            record['metrics']['runtime_seconds'] = elapsed
            records.append(record)
        if progress:
            progress(replicate + 1, config.replicates)
    return records, summarize(records, [m.key for m in config.methods], config.metrics)
