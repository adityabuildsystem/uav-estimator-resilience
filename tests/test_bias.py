import pytest
from sim.bias import GaussMarkovBias
import numpy as np

def test_bias_reproducibility():
    dt = 0.001
    tau = 1.0
    sigma_b = 0.0005
    seed = 42
    bias1 = GaussMarkovBias(dt, tau, sigma_b, seed)
    bias2 = GaussMarkovBias(dt, tau, sigma_b, seed)

    computed_bias1 = [bias1.step() for _ in range(100)]
    computed_bias2 = [bias2.step() for _ in range(100)]
    assert computed_bias1 == computed_bias2, "Bias values should be reproducible with the same seed"

def test_bias_different_seeds():
    bias1 = GaussMarkovBias(0.001, 1.0, 0.0005, 42)
    bias2 = GaussMarkovBias(0.001, 1.0, 0.0005, 99)

    computed_bias1 = [bias1.step() for _ in range(100)]
    computed_bias2 = [bias2.step() for _ in range(100)]
    assert computed_bias1 != computed_bias2, "Bias values should differ with different seeds"

def test_negative_dt():
    with pytest.raises(ValueError):
        GaussMarkovBias(-0.001, 1.0, 0.0005, 42)

def test_negative_tau():
    with pytest.raises(ValueError):
        GaussMarkovBias(0.001, -1.0, 0.0005, 42)

def test_negative_sigma_b():
    with pytest.raises(ValueError):
        GaussMarkovBias(0.001, 1.0, -0.0005, 42)

def test_zero_bias_std():
    bias = GaussMarkovBias(0.001, 1.0, 0.0, 42)
    computed_bias = [bias.step() for _ in range(100)]
    assert all(b == 0 for b in computed_bias), "Bias should remain zero when sigma_b is zero"

def test_stationary_initialization():
    initial_biases = []
    for seed in range(10000):
        model = GaussMarkovBias(0.01, 10, 0.0005, seed)
        initial_biases.append(model.bias)
    sample_mean = np.mean(initial_biases)
    sample_std = np.std(initial_biases, ddof=1)

    assert abs(sample_mean) <3*0.0005/100, f"Sample mean {sample_mean} is not close to 0"
    assert abs((sample_std - 0.0005)/0.0005) < 0.03, f"Sample std {sample_std} is not close to sigma_b"

def test_temporal_correlation():
    dt = 0.01
    tau = 10
    sigma_b = 0.0005
    samples = 100000

    bias_model = GaussMarkovBias(dt, tau, sigma_b, seed=42)
    biases = [bias_model.step() for _ in range(samples)]

    lag_one_correlation = np.corrcoef(biases[:-1], biases[1:])[0, 1]
    expected_correlation = np.exp(-dt / tau)

    assert abs(lag_one_correlation - expected_correlation) < 0.001, f"Lag-one correlation {lag_one_correlation} is not close to expected {expected_correlation}"

def test_vector_bias_shape():
    gen = GaussMarkovBias(0.01, 10, np.array([0.0005, 0.0006, 0.0004]), seed=42)

    assert gen.bias.shape == (3,)
    assert gen.step().shape == (3,)

def test_scalar_bias_returns_float():
    gen = GaussMarkovBias(0.01, 10, 0.0005, seed=42)
    assert isinstance(gen.step(), float)

def test_vector_reproducibility():
    sigma_b = np.array([0.0005, 0.0006, 0.0004])
    gen1 = GaussMarkovBias(0.01, 10, sigma_b, seed=42)
    gen2 = GaussMarkovBias(0.01, 10, sigma_b, seed=42)

    for _ in range(100):
        np.testing.assert_array_almost_equal(gen1.step(), gen2.step())

def test_vector_bias_axes_are_not_identical():
    sigma_b = np.array([0.0005, 0.0005, 0.0005])
    gen = GaussMarkovBias(0.01, 10, sigma_b, seed=42)
    samples = np.array([gen.step() for _ in range(100)])

    assert not np.array_equal(samples[:, 0], samples[:, 1])
    assert not np.array_equal(samples[:, 1], samples[:, 2])