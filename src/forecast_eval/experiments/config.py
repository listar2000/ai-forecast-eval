from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Tuple
from pathlib import Path
import yaml
from ..simulation.config import (SimulationConfig, EventConfig, ForecasterConfig,
                                  ParticipationConfig, MarketConfig, TruthConfig)
from ..evaluation.ranking import METRICS
from ..methods.registry import make_method


@dataclass(frozen=True)
class MethodConfig:
    name: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    label: str = ''

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name or not isinstance(self.parameters, dict):
            raise ValueError('Method needs a name and parameter mapping')
        if not isinstance(self.label, str):
            raise ValueError('Method label must be a string')
        if 'random_state' in self.parameters:
            raise ValueError('random_state is managed by the experiment runner')

    @property
    def key(self):
        return self.label or self.name


@dataclass(frozen=True)
class ExperimentConfig:
    seed: int = 1234
    replicates: int = 100
    mode: str = 'resample_world'
    simulation: SimulationConfig = field(default_factory=SimulationConfig)
    methods: Tuple[MethodConfig, ...] = field(default_factory=lambda: (
        MethodConfig('mean_brier'), MethodConfig('peer_brier')))
    metrics: Tuple[str, ...] = METRICS

    def __post_init__(self):
        if type(self.seed) is not int or self.seed < 0:
            raise ValueError('seed must be a nonnegative integer')
        if type(self.replicates) is not int or self.replicates < 1:
            raise ValueError('replicates must be a positive integer')
        if self.mode not in ('resample_world', 'fixed_world'):
            raise ValueError('Unknown Monte Carlo mode')
        if not self.methods or len({m.key for m in self.methods}) != len(self.methods):
            raise ValueError('Method labels must be nonempty and unique')
        if not self.metrics or len(set(self.metrics)) != len(self.metrics) or set(self.metrics) - set(METRICS):
            raise ValueError('Unknown, duplicate, or empty metric list')
        for method in self.methods:
            make_method(method.name, method.parameters)  # fail before starting a run
            if method.name == 'market_relative_brier' and not self.simulation.market.enabled:
                raise ValueError('Enable simulation.market for market_relative_brier')

    def to_dict(self):
        return asdict(self)


def config_from_dict(raw):
    if not isinstance(raw, dict):
        raise ValueError('Configuration must be a mapping')
    raw = dict(raw)
    simulation = dict(raw.pop('simulation', {}))
    constructors = {'events': EventConfig, 'forecasters': ForecasterConfig,
                    'participation': ParticipationConfig, 'market': MarketConfig, 'truth': TruthConfig}
    for key, cls in constructors.items():
        if key in simulation:
            simulation[key] = cls(**simulation[key])
    if 'methods' in raw:
        raw['methods'] = tuple(MethodConfig(**m) for m in raw['methods'])
    if 'metrics' in raw:
        raw['metrics'] = tuple(raw['metrics'])
    return ExperimentConfig(simulation=SimulationConfig(**simulation), **raw)


def load_config(path):
    return config_from_dict(yaml.safe_load(Path(path).read_text()))
