import numpy as np
import pytest
from scipy.stats import kendalltau
from forecast_eval.contracts import ObservedForecasts, RankingResult
from forecast_eval.methods.mean_brier import MeanBrier
from forecast_eval.methods.peer_brier import PeerBrier
from forecast_eval.methods.market_relative_brier import MarketRelativeBrier
from forecast_eval.evaluation.ranking import ranking_metrics
from forecast_eval.evaluation.evaluate import evaluate
from forecast_eval.simulation.generate import generate_world
from forecast_eval.simulation.config import SimulationConfig


def fixture():
    return ObservedForecasts(('a','b'), ('x','y'), [[0.8,0.2],[0.6,0.4]], [1,0], [0.5,0.5])


def test_hand_calculated_baselines():
    data = fixture()
    np.testing.assert_allclose(MeanBrier().fit(data).result().scores, [-0.04,-0.16])
    np.testing.assert_allclose(PeerBrier().fit(data).result().scores, [0.06,-0.06])
    np.testing.assert_allclose(MarketRelativeBrier().fit(data).result().scores, [0.21,0.09])
    with pytest.raises(RuntimeError):
        MeanBrier().result()


def test_empty_history_and_singletons():
    data = ObservedForecasts(('a','b'), ('x','y'), [[0.8,0.2],[np.nan,np.nan]], [1,0])
    result = MeanBrier().fit(data).result()
    assert np.isnan(result.scores[1])
    assert np.isnan(PeerBrier().fit(data).result().scores).all()
    assert all(x is None for x in ranking_metrics(result.scores, [0,0.1]).values())


def test_failed_refit_clears_old_result():
    method = MarketRelativeBrier().fit(fixture())
    data = fixture()
    with pytest.raises(ValueError):
        method.fit(ObservedForecasts(data.forecaster_ids, data.event_ids, data.forecasts, data.outcomes))
    with pytest.raises(RuntimeError):
        method.result()


def test_ranking_and_uniform_tie_breaking():
    perfect = ranking_metrics([3,2,1], [0,0.1,0.2])
    assert perfect == {'pairwise_accuracy':1, 'kendall_tau_b':1, 'best_selection':1, 'selection_regret':0}
    reverse = ranking_metrics([1,2,3], [0,0.1,0.2])
    assert reverse['kendall_tau_b'] == -1 and reverse['selection_regret'] == 0.2
    ties = ranking_metrics([1,1,1], [0,0.1,0.2])
    assert ties['pairwise_accuracy'] == 0.5 and ties['best_selection'] == 1/3
    assert ties['selection_regret'] == pytest.approx(0.1)
    assert ties['kendall_tau_b'] is None
    true_ties = ranking_metrics([3,2,1], [0,0,0.2])
    assert true_ties['best_selection'] == 1
    assert ranking_metrics([1,2], [0,0])['pairwise_accuracy'] is None


def test_kendall_matches_independent_scipy_implementation():
    rng = np.random.default_rng(99)
    for _ in range(50):
        scores, risks = rng.integers(0, 5, (2, 15))
        ours = ranking_metrics(scores, risks)['kendall_tau_b']
        assert ours == pytest.approx(kendalltau(scores, -risks).statistic)


def test_evaluator_aligns_by_ids():
    truth = generate_world(SimulationConfig(), 3).truth
    result = RankingResult(truth.forecaster_ids[::-1], -truth.risks[::-1])
    assert evaluate(result, truth)['pairwise_accuracy'] == 1
    with pytest.raises(ValueError):
        evaluate(RankingResult(('missing',), [0]), truth)
