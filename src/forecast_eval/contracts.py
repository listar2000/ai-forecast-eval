"""Public contracts. Oracle information is deliberately separate from method inputs."""
from dataclasses import dataclass, field
from typing import Any, Mapping, Optional, Tuple
import numpy as np


def readonly_array(value, dtype=float):
    array = np.array(value, dtype=dtype, copy=True)
    array.setflags(write=False)
    return array


@dataclass(frozen=True)
class ObservedForecasts:
    forecaster_ids: Tuple[str, ...]
    event_ids: Tuple[str, ...]
    forecasts: np.ndarray  # forecasters x events; NaN means unobserved
    outcomes: np.ndarray  # one shared outcome per event
    market_forecasts: Optional[np.ndarray] = None

    def __post_init__(self):
        object.__setattr__(self, 'forecaster_ids', tuple(self.forecaster_ids))
        object.__setattr__(self, 'event_ids', tuple(self.event_ids))
        q = readonly_array(self.forecasts)
        y = readonly_array(self.outcomes)
        if q.shape != (len(self.forecaster_ids), len(self.event_ids)):
            raise ValueError('Forecast shape does not match IDs')
        if not q.size or len(set(self.forecaster_ids)) != len(self.forecaster_ids) or len(set(self.event_ids)) != len(self.event_ids):
            raise ValueError('IDs must be unique and data nonempty')
        if y.shape != (len(self.event_ids),) or not np.isin(y, [0, 1]).all():
            raise ValueError('Outcomes must be a binary vector')
        observed = ~np.isnan(q)
        if not np.isfinite(q[observed]).all() or ((q[observed] < 0) | (q[observed] > 1)).any():
            raise ValueError('Observed forecasts must lie in [0, 1]')
        object.__setattr__(self, 'forecasts', q)
        object.__setattr__(self, 'outcomes', y)
        if self.market_forecasts is not None:
            m = readonly_array(self.market_forecasts)
            if m.shape != y.shape or not np.isfinite(m).all() or ((m < 0) | (m > 1)).any():
                raise ValueError('Market forecasts must be a complete probability vector')
            object.__setattr__(self, 'market_forecasts', m)


@dataclass(frozen=True)
class SimulationTruth:
    forecaster_ids: Tuple[str, ...]
    probabilities: np.ndarray
    potential_forecasts: np.ndarray
    reference_weights: np.ndarray
    risks: np.ndarray  # common-reference squared probability error; lower is better

    def __post_init__(self):
        for key in ('probabilities', 'potential_forecasts', 'reference_weights', 'risks'):
            object.__setattr__(self, key, readonly_array(getattr(self, key)))


@dataclass(frozen=True)
class RankingResult:
    forecaster_ids: Tuple[str, ...]
    scores: np.ndarray  # higher is better; NaN means not estimable
    diagnostics: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        object.__setattr__(self, 'forecaster_ids', tuple(self.forecaster_ids))
        scores = readonly_array(self.scores)
        if scores.shape != (len(self.forecaster_ids),) or np.isinf(scores).any():
            raise ValueError('Scores must be a vector of finite values or NaNs')
        if len(set(self.forecaster_ids)) != len(self.forecaster_ids):
            raise ValueError('Duplicate forecaster IDs')
        object.__setattr__(self, 'scores', scores)
