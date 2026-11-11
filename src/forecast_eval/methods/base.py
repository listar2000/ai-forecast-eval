from abc import ABC, abstractmethod
from ..contracts import ObservedForecasts, RankingResult


class RankingMethod(ABC):
    """Fit observed data and return scores where higher means better.

    Constructors accept random_state for stochastic fits. fit must reset all
    fitted state; result before fit raises RuntimeError. Never access oracle data.
    """
    def __init__(self, *, random_state=None):
        self.random_state = random_state
        self._result = None

    @abstractmethod
    def fit(self, data: ObservedForecasts) -> 'RankingMethod':
        raise NotImplementedError

    def result(self) -> RankingResult:
        if self._result is None:
            raise RuntimeError('Call fit before result')
        return self._result
