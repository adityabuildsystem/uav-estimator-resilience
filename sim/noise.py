import numpy as np
import math

class WhiteNoiseGenerator:
    def __init__(self, noise_density, sample_rate_hz, seed):

        if not math.isfinite(noise_density):
            raise ValueError("noise_density must be finite")
        if not math.isfinite(sample_rate_hz):
            raise ValueError("sample_rate_hz must be finite")

        self.noise_density = noise_density
        self.sample_rate_hz = sample_rate_hz
        self.rng = np.random.default_rng(seed)

        if noise_density < 0:
            raise ValueError("noise_density must be non-negative")
        if sample_rate_hz <= 0:
            raise ValueError("sample_rate_hz must be positive")

        self.sigma_sample = self.noise_density*np.sqrt(self.sample_rate_hz/2)


    def sample(self, size = None):
        return self.rng.normal(0, self.sigma_sample, size=size)