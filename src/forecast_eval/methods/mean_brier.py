from .base import RankingMethod
from ._utils import result_from_losses


class MeanBrier(RankingMethod):
    def fit(self, data):
        self._result = None
        self._result = result_from_losses(data, (data.forecasts - data.outcomes) ** 2)
        return self
