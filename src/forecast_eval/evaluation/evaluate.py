import numpy as np
from .ranking import ranking_metrics


def evaluate(result, truth):
    if set(result.forecaster_ids) != set(truth.forecaster_ids):
        raise ValueError('Result IDs must match the full forecaster population')
    lookup = dict(zip(result.forecaster_ids, result.scores))
    aligned = np.array([lookup[i] for i in truth.forecaster_ids])
    metrics = ranking_metrics(aligned, truth.risks)
    metrics['estimate_coverage'] = float(np.isfinite(aligned).mean())
    return metrics
