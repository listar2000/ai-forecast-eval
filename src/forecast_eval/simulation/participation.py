import numpy as np
from .config import ParticipationConfig


def generate_mask(shape, config: ParticipationConfig, rng: np.random.Generator):
    n, j = shape
    if config.mechanism == 'complete':
        return np.ones(shape, dtype=bool)
    if config.mechanism == 'random':
        return rng.random(shape) < config.observation_probability
    # Ordered entrants have fixed-length contiguous lifetimes. Forecaster order
    # is epsilon order; reverse epsilons in config to reverse the skill/time trend.
    width = max(1, int(np.ceil(j * config.active_fraction)))
    starts = np.rint(np.linspace(0, j - width, n)).astype(int)
    events = np.arange(j)[None, :]
    return (events >= starts[:, None]) & (events < (starts + width)[:, None])
