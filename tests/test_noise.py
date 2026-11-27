from sim.noise import WhiteNoiseGenerator
import numpy as np
import pytest

def test_noise_reproducibility():
    seed = 42
    noise_density = 0.1
    sample_rate_hz = 1000

    generator1 = WhiteNoiseGenerator(noise_density, sample_rate_hz, seed)
    generator2 = WhiteNoiseGenerator(noise_density, sample_rate_hz, seed)

    samples1 = [generator1.sample() for _ in range(100)]
    samples2 = [generator2.sample() for _ in range(100)]

    assert samples1 == samples2, "Samples should be reproducible with the same seed"

def test_noise_different_seeds():
    noise_density = 0.1
    sample_rate_hz = 1000

    generator1 = WhiteNoiseGenerator(noise_density, sample_rate_hz, seed=42)
    generator2 = WhiteNoiseGenerator(noise_density, sample_rate_hz, seed=99)

    samples1 = [generator1.sample() for _ in range(100)]
    samples2 = [generator2.sample() for _ in range(100)]

    assert samples1 != samples2, "Samples should differ with different seeds"

def test_noise_mean_and_standard_deviation():
    noise_density = 0.1
    sample_rate_hz = 1000
    samples = 10000

    generator = WhiteNoiseGenerator(noise_density, sample_rate_hz, seed=42)
    noise_samples = [generator.sample() for _ in range(samples)]

    sample_mean = np.mean(noise_samples)
    sample_std = np.std(noise_samples, ddof=1)

    expected_std = noise_density * np.sqrt(sample_rate_hz / 2)

    assert abs(sample_mean) < 3 * expected_std / np.sqrt(samples), f"Sample mean {sample_mean} is not close to 0"
    assert abs((sample_std - expected_std) / expected_std) < 0.03, f"Sample std {sample_std} is not close to expected std {expected_std}"

def test_uncorrelation():
    noise_density = 0.1
    sample_rate_hz = 1000
    samples = 100000

    generator = WhiteNoiseGenerator(noise_density, sample_rate_hz, seed=42)

    noise_samples = [generator.sample() for _ in range(samples)]

    autocorrelation = np.corrcoef(noise_samples[:-1], noise_samples[1:])[0, 1]
    assert abs(autocorrelation) < 0.02, f"Autocorrelation {autocorrelation} is not close to 0, indicating correlation in the noise samples"

def test_negative_noise_density():
    with pytest.raises(ValueError):
        WhiteNoiseGenerator(-0.1, 1000, seed=42)

def test_invalid_sample_rate():
    with pytest.raises(ValueError):
        WhiteNoiseGenerator(0.1, 0, seed=42)
    with pytest.raises(ValueError):
        WhiteNoiseGenerator(0.1, -1000, seed=42)

def test_zero_noise_density():
    generator = WhiteNoiseGenerator(0.0, 1000, seed=42)
    samples = [generator.sample() for _ in range(100)]
    assert all(sample == 0.0 for sample in samples), "All samples should be zero when noise density is zero"

def test_vector_noise_shape():
    gen = WhiteNoiseGenerator(0.005, 100,42)
    noise = gen.sample(size=3)
    assert noise.shape == (3,)