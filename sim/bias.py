import math
import numpy as np
class GaussMarkovBias:
    def __init__(self, dt, tau, sigma_b, seed):

        if not math.isfinite(dt) or dt <= 0:
            raise ValueError("dt must be finite and positive")
        if not math.isfinite(tau) or tau <= 0:
            raise ValueError("tau must be finite and positive")
        if not np.all(np.isfinite(sigma_b)):
            raise ValueError("sigma_b must be finite")
        if np.any(np.array(sigma_b) < 0):
            raise ValueError("sigma_b must be non-negative")

        self.dt = dt
        self.tau = tau
        self.sigma_b = np.array(sigma_b, dtype=float)

        if self.sigma_b.ndim >1:
            raise ValueError("sigma_b must be a scalar or 1D array")
        if self.sigma_b.ndim == 1 and self.sigma_b.shape !=(3,):
            raise ValueError("sigma_b must contain exactly 3 elements.")

        self.phi = math.exp(-self.dt / self.tau)
        self.sigma_w = self.sigma_b * math.sqrt(1 - self.phi**2)

        self.rng = np.random.default_rng(seed)
        self.bias = self.rng.normal(0, self.sigma_b)
    
    def step(self):
        w = self.rng.normal(0, self.sigma_w)
        self.bias = self.phi * self.bias + w

        if np.ndim(self.bias) == 0:
            return float(self.bias)

        return self.bias