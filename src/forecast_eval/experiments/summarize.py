from itertools import combinations
import numpy as np


def estimate(values):
    values = np.array([v for v in values if v is not None], float)
    if not len(values):
        return {'mean': None, 'mcse': None, 'n_valid': 0}
    return {'mean': float(values.mean()),
            'mcse': float(values.std(ddof=1) / np.sqrt(len(values))) if len(values) > 1 else None,
            'n_valid': len(values)}


def summarize(records, method_keys, metrics):
    output = {}
    for key in method_keys:
        rows = [r for r in records if r['method'] == key]
        output[key] = {
            'replicates': len(rows),
            'fit_failures': sum(r['status'] == 'failed' for r in rows),
            'partial_rankings': sum(r['status'] == 'partial' for r in rows),
            'metrics': {m: estimate([r['metrics'].get(m) for r in rows])
                        for m in list(metrics) + ['estimate_coverage', 'runtime_seconds']}}
    paired = []
    for left, right in combinations(method_keys, 2):
        a = {r['replicate']: r for r in records if r['method'] == left}
        b = {r['replicate']: r for r in records if r['method'] == right}
        diffs = {}
        for metric in metrics:
            values = []
            for replicate in sorted(a.keys() & b.keys()):
                x, y = a[replicate]['metrics'].get(metric), b[replicate]['metrics'].get(metric)
                if x is not None and y is not None:
                    values.append(x - y)
            diffs[metric] = estimate(values)
        paired.append({'left': left, 'right': right, 'difference': 'left minus right', 'metrics': diffs})
    return {'methods': output, 'paired_differences': paired,
            'notes': 'Ranking metrics require complete estimates; means condition on valid replicates. '
                     'Inspect n_valid, fit_failures, and partial_rankings. MCSE is simulation sampling error, '
                     'not a confidence interval for an individual fitted skill. Lower regret/runtime is better; '
                     'higher accuracy/tau/best-selection/coverage is better.'}
