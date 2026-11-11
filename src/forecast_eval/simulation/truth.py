import numpy as np
from ..contracts import SimulationTruth


def compute_truth(ids, probabilities, forecasts):
    weights = np.full(len(probabilities), 1.0 / len(probabilities))
    risks = ((forecasts - probabilities[None, :]) ** 2) @ weights
    return SimulationTruth(ids, probabilities, forecasts, weights, risks)
