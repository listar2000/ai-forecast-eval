"""Validated, explicit components for the initial simulation family."""
from dataclasses import dataclass, field
from typing import Tuple
import math


def probability(x, name):
    if not isinstance(x, (int, float)) or isinstance(x, bool) or not math.isfinite(x) or not 0 <= x <= 1:
        raise ValueError(f'{name} must be a finite probability')


@dataclass(frozen=True)
class EventConfig:
    generator: str = 'uniform'
    count: int = 1000
    probability_range: Tuple[float, float] = (0.2, 0.8)

    def __post_init__(self):
        if self.generator != 'uniform':
            raise ValueError('Unknown event generator')
        if type(self.count) is not int or self.count < 1:
            raise ValueError('Event count must be a positive integer')
        if len(self.probability_range) != 2:
            raise ValueError('probability_range must have two endpoints')
        lo, hi = self.probability_range
        probability(lo, 'lower endpoint'); probability(hi, 'upper endpoint')
        if lo > hi:
            raise ValueError('Invalid probability range')


@dataclass(frozen=True)
class ForecasterConfig:
    generator: str = 'additive_error'
    epsilons: Tuple[float, ...] = (0.0, 0.025, 0.05, 0.1, 0.15)
    sign_policy: str = 'independent_symmetric'

    def __post_init__(self):
        if self.generator != 'additive_error' or self.sign_policy != 'independent_symmetric':
            raise ValueError('Unknown forecaster generator or sign policy')
        if len(self.epsilons) < 2:
            raise ValueError('At least two forecasters are required')
        for epsilon in self.epsilons:
            probability(epsilon, 'epsilon')


@dataclass(frozen=True)
class ParticipationConfig:
    mechanism: str = 'complete'
    observation_probability: float = 0.5
    active_fraction: float = 0.6

    def __post_init__(self):
        if self.mechanism not in ('complete', 'random', 'staggered'):
            raise ValueError('Unknown participation mechanism')
        probability(self.observation_probability, 'observation_probability')
        probability(self.active_fraction, 'active_fraction')
        if self.active_fraction == 0:
            raise ValueError('active_fraction must be positive')


@dataclass(frozen=True)
class MarketConfig:
    enabled: bool = False
    epsilon: float = 0.1

    def __post_init__(self):
        if type(self.enabled) is not bool:
            raise ValueError('market.enabled must be boolean')
        probability(self.epsilon, 'market epsilon')


@dataclass(frozen=True)
class TruthConfig:
    target: str = 'mean_squared_probability_error'
    reference_weights: str = 'uniform'

    def __post_init__(self):
        if self.target != 'mean_squared_probability_error' or self.reference_weights != 'uniform':
            raise ValueError('Only uniform common-reference probability-error risk is implemented')


@dataclass(frozen=True)
class SimulationConfig:
    events: EventConfig = field(default_factory=EventConfig)
    forecasters: ForecasterConfig = field(default_factory=ForecasterConfig)
    participation: ParticipationConfig = field(default_factory=ParticipationConfig)
    market: MarketConfig = field(default_factory=MarketConfig)
    truth: TruthConfig = field(default_factory=TruthConfig)

    def __post_init__(self):
        lo, hi = self.events.probability_range
        errors = list(self.forecasters.epsilons)
        if self.market.enabled:
            errors.append(self.market.epsilon)
        if max(errors) > lo or max(errors) + hi > 1:
            raise ValueError('Additive errors would leave [0, 1]; narrow errors or probability range (no clipping)')
