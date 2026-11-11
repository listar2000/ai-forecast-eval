from .base import RankingMethod
from ._utils import result_from_losses


class MarketRelativeBrier(RankingMethod):
    def fit(self, data):
        self._result = None
        if data.market_forecasts is None:
            raise ValueError('MarketRelativeBrier requires market forecasts')
        loss = (data.forecasts - data.outcomes) ** 2
        market_loss = (data.market_forecasts - data.outcomes) ** 2
        self._result = result_from_losses(data, loss - market_loss)
        return self
