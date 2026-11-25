# Gyroscope Bias Model — First-Order Gauss-Markov Process

## 1. Purpose

This module implements a stochastic gyroscope bias model for the UAV estimator resilience simulation.

A gyroscope measures angular velocity. Its output can contain a slowly varying bias in addition to the true angular rate and measurement noise.

If this bias is ignored, an attitude estimator may accumulate orientation error over time, particularly when angular rate measurements are integrated.

The purpose of this model is to introduce temporally correlated bias into simulated gyroscope measurements so that estimator performance can be evaluated under more realistic error conditions than a constant-bias or independent-white-noise-only model.

This is a simulation component, not a flight-certified sensor model.

## 2. Physical intuition

Gyroscope bias is not necessarily independent from one sample to the next.

For example, temperature changes, internal sensor effects, and other low-frequency mechanisms can cause bias to evolve gradually rather than jump randomly at every measurement.

A first-order Gauss-Markov process represents this behavior using a mean-reverting stochastic process.

The bias tends to retain its previous value over short time intervals, while gradually returning toward its long-term mean.

For this implementation, the long-term mean is zero.

The parameter `tau` controls how quickly the process loses memory of its previous value:

- A smaller `tau` produces faster bias variation.
- A larger `tau` produces slower, more strongly correlated bias variation.

The stationary standard deviation controls the overall spread of the bias values.

## 3. Mathematical model

### 3.1 Continuous-time model

The first-order Gauss-Markov process is represented by:

$\[
db(t)=-\frac{1}{\tau}b(t)\,dt+
\sqrt{\frac{2\sigma_b^2}{\tau}}\,dW(t)
\]$

Where:

- \(b(t)\) is the gyroscope bias.
- \(\tau\) is the correlation time constant.
- \(\sigma_b\) is the stationary bias standard deviation.
- \(W(t)\) is a standard Wiener process.

The first term represents mean reversion. The second term introduces stochastic variation.

### 3.2 Discrete-time model

The simulation operates at discrete time intervals, so the continuous model is converted into an exact discrete-time transition:

$\[
b_{k+1}=\phi b_k+w_k
\]$

The transition coefficient is:

$\[
\phi=e^{-\Delta t/\tau}
\]$

The innovation is Gaussian:

$\[
w_k\sim\mathcal{N}(0,\sigma_w^2)
\]$

Its standard deviation is:

$\[
\sigma_w=\sigma_b\sqrt{1-\phi^2}
\]$

This choice preserves the stationary variance of the continuous-time process when sampled at interval \(\Delta t\).

The implementation calculates \(\phi\) and \(\sigma_w\) once during object initialization because they remain constant for a fixed set of model parameters.

## 4. Model parameters

| Parameter | Meaning | Units |
|---|---|---|
| `dt` | Simulation time step | seconds |
| `tau` | Bias correlation time constant | seconds |
| `sigma_b` | Stationary bias standard deviation | rad/s |
| `seed` | Random-number generator seed | dimensionless |

### Current provisional parameters

| Parameter | Value |
|---|---:|
| `dt` | 0.01 s |
| `tau` | 10 s |
| `sigma_b` | 0.0005 rad/s |
| `seed` | 42 |

These values are provisional simulation assumptions, not measured specifications for a particular gyroscope.

The stationary bias standard deviation and the per-step innovation standard deviation are different quantities. The innovation standard deviation depends on both the sampling interval and the correlation time constant.

## 5. Initialization

The initial bias is drawn from the stationary distribution:

$\[
b_0\sim\mathcal{N}(0,\sigma_b^2)
\]$

This avoids an artificial startup transient that would occur if every simulation began at zero and then gradually approached the stationary distribution.

For reproducibility, the implementation uses NumPy's `default_rng(seed)` random-number generator.

Identical seeds, parameters, and random-number call sequences produce identical simulated sequences.

## 6. Verification

The component is verified using automated tests and separate statistical experiments.

### 6.1 Reproducibility

Two instances configured with identical parameters and random seeds produce identical bias sequences.

### 6.2 Different seeds

The tested different seeds produce different sequences.

This checks deterministic seed behavior; it is not a proof of statistical independence.

### 6.3 Parameter validation

The constructor rejects:

- Non-positive time steps.
- Non-positive correlation time constants.
- Negative stationary bias standard deviations.
- Non-finite model parameters.

A zero stationary bias standard deviation is permitted and produces a zero-bias process.

### 6.4 Stationary initialization

An experiment using 10,000 independently seeded instances checks whether the initial bias samples have approximately:

- Zero mean.
- Standard deviation equal to `sigma_b`.

### 6.5 Temporal correlation

The theoretical lag-\(k\) correlation is:

$\[
\rho_k=e^{-k\Delta t/\tau}
\]$

At lag one:

$\[
\rho_1=e^{-\Delta t/\tau}
\]$

The measured lag-one correlation is compared with this theoretical value using a numerical tolerance.

These tests provide evidence of correct implementation behavior for the tested conditions. They do not establish physical fidelity to a real sensor.

## 7. Limitations

This implementation is a simplified stochastic model.

It does not independently model:

- Gyroscope white measurement noise.
- Scale-factor error.
- Axis misalignment.
- Temperature-dependent bias.
- Quantization.
- Sensor saturation.
- Vibration sensitivity.
- Complete Allan variance or Allan deviation behavior.

The Gauss-Markov model is useful for representing a temporally correlated bias process, but it does not reproduce every possible inertial sensor error mechanism.

The parameters used here are provisional and have not been fitted to real sensor characterization data.

The component is intended for estimator simulation and verification experiments. It is not a certified safety or flight-control component.

## 8. Integration into the IMU model

The bias generator is intended to be used as one component of a gyroscope measurement model.

Conceptually:

$\[
\omega_m=\omega_{\text{true}}+b+n
\]$

Where:

- $\(\omega_m\)$ is the measured angular rate.
- $\(\omega_{\text{true}}\)$ is the true angular rate.
- $\(b\)$ is the slowly varying Gauss-Markov bias.
- $\(n\)$ is the gyroscope white measurement noise.

The bias generator produces $\(b\)$ only. The true angular rate and white measurement noise will be handled by the broader IMU simulation.
