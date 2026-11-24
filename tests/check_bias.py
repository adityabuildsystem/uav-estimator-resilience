import statistics as stats
import numpy as np
import matplotlib.pyplot as plt

from sim.bias import GaussMarkovBias


def plot_bias_comparison():

    dt = 0.01
    samples = 12000

    bias1 = GaussMarkovBias(dt, 10, 0.0005, 42)
    biases1 = [bias1.step() for _ in range(samples)]

    bias2 = GaussMarkovBias(dt, 100, 0.0005, 42)
    biases2 = [bias2.step() for _ in range(samples)]

    # Each step() returns the bias at the end of its time interval.
    time = np.arange(1, samples + 1) * dt

    plt.figure(figsize=(10, 5))

    plt.plot(time, biases1, label="Tau = 10 s", linewidth=1)
    plt.plot(time, biases2, label="Tau = 100 s",
             color="orange", linewidth=1)

    plt.xlabel("Time (s)")
    plt.ylabel("Gyroscope Bias (rad/s)")
    plt.title("First-Order Gauss-Markov Bias Comparison")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("gyro_bias_comparison.png", dpi=150)
    plt.show()


def verify_stationary_initialization():
    dt = 0.01
    tau = 10
    sigma_b = 0.0005
    samples = 10000

    initial_biases = []
    for seed in range(samples):
        model = GaussMarkovBias(dt, tau, sigma_b, seed)
        initial_biases.append(model.bias)

    print(f"Sample mean: {stats.mean(initial_biases):.6f}, Sample std: {stats.stdev(initial_biases):.8f}")
              
def verify_temporal_correlation():
    dt = 0.01
    tau = 10
    sigma_b = 0.0005
    samples = 100000

    bias_model = GaussMarkovBias(dt, tau, sigma_b, seed=42)
    biases = [bias_model.step() for _ in range(samples)]

    lag_one_correlation = np.corrcoef(biases[:-1], biases[1:])[0, 1]
    print(f"Lag-1 Correlation: {lag_one_correlation:.6f}")

verify_temporal_correlation()