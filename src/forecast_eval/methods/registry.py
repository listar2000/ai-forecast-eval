from .base import RankingMethod
from .mean_brier import MeanBrier
from .peer_brier import PeerBrier
from .market_relative_brier import MarketRelativeBrier

METHODS = {'mean_brier': MeanBrier, 'peer_brier': PeerBrier,
           'market_relative_brier': MarketRelativeBrier}


def register_method(name, method_class):
    if name in METHODS:
        raise ValueError(f'Method already registered: {name}')
    if not issubclass(method_class, RankingMethod):
        raise TypeError('Methods must subclass RankingMethod')
    METHODS[name] = method_class


def make_method(name, parameters=None, random_state=None):
    if name not in METHODS:
        raise ValueError(f'Unknown method: {name}')
    return METHODS[name](random_state=random_state, **(parameters or {}))
