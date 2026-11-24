import math
import numpy as np
class GaussMarkovBias:
    def __init__(self, dt, tau, sigma_b, seed):

        if dt <= 0:
            raise ValueError("dt must be positive")
        if tau <= 0:
            raise ValueError("tau must be positive")
        if sigma_b < 0:
            raise ValueError("sigma_b must be non-negative")
        
        self.dt = dt
        self.tau = tau
        self.sigma_b = sigma_b

        self.phi = math.exp(-self.dt / self.tau)
        self.sigma_w = self.sigma_b * math.sqrt(1 - self.phi**2)

        self.rng = np.random.default_rng(seed)
        self.bias = self.rng.normal(0, sigma_b)
    
    def step(self):
        w = self.rng.normal(0, self.sigma_w)
        self.bias = self.phi * self.bias + w
        return self.bias