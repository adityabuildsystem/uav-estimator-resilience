import numpy as np

from sim.bias import GaussMarkovBias
from sim.noise import WhiteNoiseGenerator

class Accelerometer:
    def __init__(self,dt,tau,bias_std,noise_density, seed):
        self.dt = dt
        self.bias = GaussMarkovBias(dt,tau,bias_std, seed)
        self.noise = WhiteNoiseGenerator(noise_density, 1/dt, seed+1)

    def sample(self,true_specific_force):
        true_specific_force=np.asarray(true_specific_force, dtype=float)

        if true_specific_force.shape !=(3,):
            raise ValueError("true_specific_force must have shape (3,)")
        if not np.all(np.isfinite(true_specific_force)):
            raise ValueError("true_specific_value must be finite value")

        bias = self.bias.step()
        noise = self.noise.sample(3)

        return true_specific_force + bias + noise