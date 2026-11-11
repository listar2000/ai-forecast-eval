import numpy as np
from .config import EventConfig


def generate_events(config: EventConfig, rng: np.random.Generator):
    return rng.uniform(*config.probability_range, size=config.count)
