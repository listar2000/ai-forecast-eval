from dataclasses import dataclass
import numpy as np
from ..contracts import ObservedForecasts, SimulationTruth, readonly_array
from .config import SimulationConfig
from .events import generate_events
from .forecasters import generate_forecasts, generate_market
from .participation import generate_mask
from .outcomes import sample_outcomes
from .truth import compute_truth


@dataclass(frozen=True)
class SimulationWorld:
    truth: SimulationTruth
    mask: np.ndarray
    market_forecasts: object

    def observe(self, rng):
        truth = self.truth
        return ObservedForecasts(
            truth.forecaster_ids,
            tuple(f'event_{j:05d}' for j in range(len(truth.probabilities))),
            np.where(self.mask, truth.potential_forecasts, np.nan),
            sample_outcomes(truth.probabilities, rng), self.market_forecasts)


def generate_world(config: SimulationConfig, seed):
    streams = [np.random.default_rng(s) for s in np.random.SeedSequence(seed).spawn(4)]
    p = generate_events(config.events, streams[0])
    q = generate_forecasts(p, config.forecasters, streams[1])
    mask = generate_mask(q.shape, config.participation, streams[2])
    market = generate_market(p, config.market, streams[3])
    ids = tuple(f'forecaster_{i:03d}' for i in range(len(q)))
    truth = compute_truth(ids, p, q)
    return SimulationWorld(truth, readonly_array(mask, bool), None if market is None else readonly_array(market))
