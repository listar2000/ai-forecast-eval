import numpy as np
import pytest
from dataclasses import replace
from forecast_eval.simulation.config import SimulationConfig, ParticipationConfig, EventConfig, ForecasterConfig
from forecast_eval.simulation.generate import generate_world
from forecast_eval.experiments.config import config_from_dict
from forecast_eval.contracts import ObservedForecasts


def test_oracle_and_brier_identity():
    config = SimulationConfig()
    world = generate_world(config, 7)
    p, q = world.truth.probabilities, world.truth.potential_forecasts
    np.testing.assert_allclose(world.truth.risks, np.array(config.forecasters.epsilons) ** 2, atol=1e-15)
    exact = p * (q - 1) ** 2 + (1 - p) * q ** 2
    np.testing.assert_allclose(exact, p * (1-p) + (q-p) ** 2)
    assert q.min() >= 0 and q.max() <= 1


def test_mask_does_not_change_truth_or_other_streams():
    full = generate_world(SimulationConfig(), 10)
    sparse = generate_world(replace(SimulationConfig(), participation=ParticipationConfig('random', 0.2)), 10)
    np.testing.assert_array_equal(full.truth.potential_forecasts, sparse.truth.potential_forecasts)
    np.testing.assert_array_equal(full.truth.risks, sparse.truth.risks)
    a = full.observe(np.random.default_rng(3))
    b = sparse.observe(np.random.default_rng(3))
    np.testing.assert_array_equal(a.outcomes, b.outcomes)
    assert 0.15 < sparse.mask.mean() < 0.25
    assert not hasattr(b, 'probabilities')
    assert np.isnan(b.forecasts[~sparse.mask]).all()
    with pytest.raises(ValueError):
        b.forecasts[0, 0] = 0.5


def test_staggered_windows():
    cfg = replace(SimulationConfig(), participation=ParticipationConfig('staggered', active_fraction=0.4))
    world = generate_world(cfg, 4)
    assert (world.mask.sum(axis=1) == 400).all()
    assert world.mask[0, 0] and world.mask[-1, -1]
    assert not world.mask[0, -1]


@pytest.mark.parametrize('raw', [
    {'replicates': 0}, {'seed': -1}, {'mode': 'oops'}, {'unknown': 1},
    {'simulation': {'events': {'count': 0}}},
    {'simulation': {'events': {'probability_range': [0, 1]}}},
    {'simulation': {'forecasters': {'epsilons': [0, float('nan')]}}},
    {'simulation': {'participation': {'mechanism': 'oops'}}},
    {'methods': [{'name': 'missing'}]},
    {'methods': [{'name': 'mean_brier'}, {'name': 'mean_brier'}]},
    {'methods': [{'name': 'market_relative_brier'}]},
    {'metrics': ['not_a_metric']},
])
def test_invalid_configs(raw):
    with pytest.raises((ValueError, TypeError)):
        config_from_dict(raw)


def test_observation_validation():
    with pytest.raises(ValueError):
        ObservedForecasts(('a',), ('x',), [[1.1]], [1])
    with pytest.raises(ValueError):
        ObservedForecasts(('a',), ('x',), [[0.5]], [0.5])


def test_valid_boundary_and_invalid_overflow():
    valid = SimulationConfig(events=EventConfig(probability_range=(0.8,0.8)),
                             forecasters=ForecasterConfig(epsilons=(0,0.2)))
    data = generate_world(valid, 33).observe(np.random.default_rng(0))
    assert data.forecasts.max() == 1
    with pytest.raises(ValueError):
        SimulationConfig(events=EventConfig(probability_range=(0.8,0.8)),
                         forecasters=ForecasterConfig(epsilons=(0,0.200000000000005)))
