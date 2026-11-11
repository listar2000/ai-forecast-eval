import hashlib
import numpy as np


def method_seed(seed, replicate, label):
    # Python hash() is process-randomized; a stable digest makes order irrelevant.
    digest = hashlib.sha256(label.encode()).digest()
    words = [int.from_bytes(digest[i:i+4], 'little') for i in range(0, 16, 4)]
    return int(np.random.SeedSequence([seed, 2, replicate] + words).generate_state(1)[0])


def outcome_rng(seed, replicate):
    return np.random.default_rng(np.random.SeedSequence([seed, 1, replicate]))
