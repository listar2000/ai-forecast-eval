# Simulation

[generate.py](generate.py) assembles a world from independent random streams. Calling `world.observe(rng)` samples one outcome per event and exposes each forecaster’s selected predictions.

| File | Responsibility |
| --- | --- |
| [config.py](config.py) | Validate generator names, parameters, and probability bounds |
| [events.py](events.py) and [forecasters.py](forecasters.py) | Draw event probabilities, potential forecasts, and the optional market forecast |
| [participation.py](participation.py) | Select the forecaster–event pairs that will be observed |
| [outcomes.py](outcomes.py) and [truth.py](truth.py) | Sample binary outcomes and compute oracle risks on the common event set |

**Add a setting.** To vary coverage, copy the [random missingness config](../../../configs/random_missingness.yaml) and change `simulation.participation.observation_probability`. For a new participation mechanism, accept its name and parameters in `ParticipationConfig`, then implement its branch in `generate_mask`. Return a boolean mask shaped like the full forecast matrix and use the supplied RNG. Check the expected coverage and confirm that changing only participation preserves oracle risks. See the [simulation tests](../../../tests/test_simulation.py).
