"""Common ranking metrics, with uniform tie-breaking for winner selection."""
import numpy as np

METRICS = ('pairwise_accuracy', 'kendall_tau_b', 'best_selection', 'selection_regret')
TOLERANCE = 1e-12


def ranking_metrics(scores, risks):
    scores, risks = np.asarray(scores, float), np.asarray(risks, float)
    if scores.shape != risks.shape or scores.ndim != 1 or len(scores) < 2:
        raise ValueError('Need matching vectors for at least two forecasters')
    if not np.isfinite(risks).all():
        raise ValueError('Oracle risks must be finite')
    # Partial rankings are deliberately not graded as if omitted models vanished.
    if not np.isfinite(scores).all():
        return {key: None for key in METRICS}
    i, j = np.triu_indices(len(scores), 1)
    sd, rd = scores[i] - scores[j], risks[j] - risks[i]
    ss = np.where(np.abs(sd) <= TOLERANCE, 0, np.sign(sd))
    rs = np.where(np.abs(rd) <= TOLERANCE, 0, np.sign(rd))
    comparable = rs != 0
    accuracy = float(np.mean(np.where(ss[comparable] == 0, 0.5,
                                      ss[comparable] == rs[comparable]))) if comparable.any() else None
    denominator = np.sqrt(float(np.count_nonzero(ss) * np.count_nonzero(rs)))
    tau = float(np.sum(ss * rs) / denominator) if denominator else None
    winners = scores >= scores.max() - TOLERANCE
    best = risks <= risks.min() + TOLERANCE
    return {'pairwise_accuracy': accuracy, 'kendall_tau_b': tau,
            'best_selection': float(best[winners].mean()),
            'selection_regret': float(np.maximum(risks[winners] - risks.min(), 0).mean())}
