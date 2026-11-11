import numpy as np
from .config import ForecasterConfig, MarketConfig


def generate_forecasts(probabilities, config: ForecasterConfig, rng: np.random.Generator):
    signs = rng.choice([-1.0, 1.0], size=(len(config.epsilons), len(probabilities)))
    return probabilities[None, :] + np.asarray(config.epsilons)[:, None] * signs


def generate_market(probabilities, config: MarketConfig, rng: np.random.Generator):
    if not config.enabled:
        return None
    return probabilities + config.epsilon * rng.choice([-1.0, 1.0], size=len(probabilities))
