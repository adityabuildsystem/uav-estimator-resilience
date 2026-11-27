from sim.bias import GaussMarkovBias
from sim.noise import WhiteNoiseGenerator
import numpy as np
class Gyroscope:
    def __init__(self, dt, tau, bias_std, noise_density, seed):
        self.dt = dt
        self.tau = tau
        self.bias_std = bias_std
        self.noise_density = noise_density

        self.bias = GaussMarkovBias(self.dt, self.tau, self.bias_std, seed)
        self.noise = WhiteNoiseGenerator(self.noise_density, 1/self.dt , seed + 1)


    def sample(self, true_rate):
        true_rate = np.array(true_rate, dtype=float)

        if true_rate.shape != (3,):
            raise ValueError("true_rate must have the shape (3,)")

        bias = self.bias.step()
        noise = self.noise.sample(3)
        return true_rate+bias+noise