import numpy as np
from ..contracts import RankingResult


def result_from_losses(data, losses):
    observed = np.isfinite(losses)
    counts = observed.sum(axis=1)
    means = np.divide(np.nansum(losses, axis=1), counts,
                      out=np.full(len(counts), np.nan), where=counts > 0)
    return RankingResult(data.forecaster_ids, -means,
                         {'observation_counts': counts.tolist()})
