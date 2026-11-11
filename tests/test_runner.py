import json
from dataclasses import replace
import numpy as np
import pytest
from forecast_eval.experiments.config import ExperimentConfig, MethodConfig, load_config
from forecast_eval.experiments.runner import run_experiment
from forecast_eval.experiments.artifacts import write_artifacts, clean
from forecast_eval.experiments.summarize import estimate
from forecast_eval.methods.base import RankingMethod
from forecast_eval.methods.registry import METHODS
from forecast_eval.contracts import RankingResult
from forecast_eval.cli import main


def scientific(records):
    rows = clean(records)
    for r in rows:
        del r['metrics']['runtime_seconds']
    return rows


def test_reproducibility_order_and_extension():
    config = ExperimentConfig(replicates=4)
    a, _ = run_experiment(config)
    b, _ = run_experiment(config)
    assert scientific(a) == scientific(b)
    c, _ = run_experiment(replace(config, methods=config.methods[::-1]))
    assert sorted(scientific(a),key=lambda r:(r['replicate'],r['method'])) == sorted(scientific(c),key=lambda r:(r['replicate'],r['method']))
    longer, _ = run_experiment(replace(config, replicates=6))
    assert scientific(a) == scientific(longer[:len(a)])


def test_fixed_world_and_paired_equivalence():
    config = replace(load_config('configs/fixed_world.yaml'), replicates=8)
    rows, summary = run_experiment(config)
    assert all(r['world_seed'] == [config.seed,0,0] for r in rows)
    assert any(r['scores'] != rows[0]['scores'] for r in rows if r['method']=='mean_brier')
    for pair in summary['paired_differences']:
        for item in pair['metrics'].values():
            assert item['mean'] == 0 and item['mcse'] == 0


def test_failures_recorded_without_losing_other_methods(monkeypatch):
    class Broken(RankingMethod):
        def fit(self, data):
            raise RuntimeError('deliberate failure')
    monkeypatch.setitem(METHODS, 'broken', Broken)
    cfg = ExperimentConfig(replicates=3, methods=(MethodConfig('mean_brier'), MethodConfig('broken')))
    rows, summary = run_experiment(cfg)
    assert summary['methods']['broken']['fit_failures'] == 3
    assert summary['methods']['mean_brier']['fit_failures'] == 0
    assert all('deliberate failure' in r['error'] for r in rows if r['method']=='broken')


def test_stochastic_method_reproducibility(monkeypatch):
    class RandomMethod(RankingMethod):
        def fit(self, data):
            self._result = RankingResult(data.forecaster_ids, np.random.default_rng(self.random_state).normal(size=len(data.forecaster_ids)))
            return self
    monkeypatch.setitem(METHODS, 'random_test', RandomMethod)
    cfg = ExperimentConfig(replicates=3, methods=(MethodConfig('random_test'),))
    assert scientific(run_experiment(cfg)[0]) == scientific(run_experiment(cfg)[0])


def test_artifacts_and_no_overwrite(tmp_path):
    cfg = ExperimentConfig(replicates=2)
    rows, summary = run_experiment(cfg)
    out = tmp_path/'run'
    write_artifacts(out, cfg, rows, summary)
    assert json.loads((out/'config.json').read_text())['seed'] == cfg.seed
    assert len((out/'replicates.jsonl').read_text().splitlines()) == 4
    assert json.loads((out/'metadata.json').read_text())['source_sha256']
    with pytest.raises(FileExistsError):
        write_artifacts(out, cfg, rows, summary)


def test_mcse_uses_sample_variance():
    result = estimate([1,2,3,None])
    assert result['mean'] == 2 and result['mcse'] == pytest.approx(1 / np.sqrt(3))
    assert result['n_valid'] == 3
    assert estimate([1])['mcse'] is None


def test_cli(tmp_path):
    path = tmp_path/'config.yaml'
    path.write_text('replicates: 2\n')
    assert main([str(path),'--output',str(tmp_path/'run')]) == 0
    with pytest.raises(SystemExit):
        main([str(path),'--output',str(tmp_path/'run')])


def test_invalid_yaml_has_cli_error(tmp_path):
    path = tmp_path/'bad.yaml'
    path.write_text('replicates: [broken\n')
    with pytest.raises(SystemExit) as caught:
        main([str(path), '--output', str(tmp_path/'run')])
    assert caught.value.code == 2
