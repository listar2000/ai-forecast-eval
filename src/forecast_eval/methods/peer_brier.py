import numpy as np
from .base import RankingMethod
from ._utils import result_from_losses


class PeerBrier(RankingMethod):
    """Subtract event mean Brier loss INCLUDING self; not Metaculus Peer Score.

    Singleton events are excluded: they provide no peer comparison. Scores
    across disconnected participation groups are not identified as common skill.
    """
    def fit(self, data):
        self._result = None
        loss = (data.forecasts - data.outcomes) ** 2
        counts = np.isfinite(loss).sum(axis=0)
        mean = np.divide(np.nansum(loss, axis=0), counts,
                         out=np.full(len(counts), np.nan), where=counts >= 2)
        self._result = result_from_losses(data, loss - mean)
        return self
