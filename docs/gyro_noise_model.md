# Gyroscope White Measurement Noise Model

## 1. Purpose

This document describes the gyroscope white measurement noise model implemented in `sim/noise.py`.

A physical gyroscope does not produce perfectly accurate angular velocity measurements. Even when the true angular velocity is constant, the measured output contains random fluctuations caused by sensor electronics and other measurement processes.

The purpose of this module is to simulate these random fluctuations so that the performance and robustness of attitude estimators can be evaluated under noisy measurement conditions.

The white-noise generator is designed as an independent component of the IMU simulation. It generates one random measurement-noise sample at each simulation time step.

It does not generate the true angular velocity or the slowly varying gyroscope bias.

## 2. Physical Intuition

Gyroscope measurement errors can contain different stochastic components.

Two important components represented in this project are:

1. **White measurement noise:** Random fluctuations that vary from sample to sample.
2. **Gyroscope bias:** A slowly varying error that can persist across multiple consecutive samples.

These components have different temporal characteristics.

White measurement noise is modeled as independent, identically distributed Gaussian random samples. Ideally, consecutive samples have zero correlation.

Gyroscope bias, on the other hand, is modeled using a first-order Gauss-Markov process. Its current value depends on its previous value, producing temporal correlation.

Keeping these components separate allows their parameters to be adjusted, tested, and fault-injected independently.

## 3. Mathematical Model

### 3.1 Gaussian White Noise

The discrete-time measurement noise is modeled as a zero-mean Gaussian random variable:

$n_k \sim \mathcal{N}(0,\sigma_n^2)$

Where:

- $n_k$ is the noise value at sample $k$.
- $\sigma_n$ is the standard deviation of the discrete noise samples.
- The mean of the noise distribution is zero.

The generated samples are assumed to be statistically independent:

$E[n_k n_{k-j}] = 0,\quad j \neq 0$

This represents ideal discrete-time white noise.

### 3.2 Noise Density

Gyroscope noise density describes the noise level relative to the measurement bandwidth.

The noise density parameter is represented by:

$N_g$

Its units are:

$\text{rad/s}/\sqrt{\text{Hz}}$

For ideal white noise, the RMS noise increases with the square root of the effective bandwidth.

Under the one-sided noise-density convention and the assumed Nyquist bandwidth:

$\sigma_n = N_g\sqrt{\frac{f_s}{2}}$

Where:

- $N_g$ is the gyroscope noise density.
- $f_s$ is the sampling frequency in Hz.
- $\sigma_n$ is the standard deviation of an individual discrete-time noise sample.

The resulting sample standard deviation has units of:

$\text{rad/s}$

### 3.3 Numerical Example

The current project configuration specifies:

- Noise density: $N_g = 0.005\ \text{rad/s}/\sqrt{\text{Hz}}$
- Sampling frequency: $f_s = 100\ \text{Hz}$

Substituting these values:

$\sigma_n = 0.005\sqrt{\frac{100}{2}}$

Therefore:

$\sigma_n \approx 0.0353553\ \text{rad/s}$

This is the standard deviation used by the random-noise generator for each simulated sample.

## 4. Model Parameters

The `WhiteNoiseGenerator` class accepts the following parameters:

| Parameter | Description | Units |
|---|---|---|
| `noise_density` | Gyroscope white-noise density | rad/s/√Hz |
| `sample_rate_hz` | Sampling frequency | Hz |
| `seed` | Random-number generator seed | Dimensionless |

### 4.1 Noise Density

The noise density determines the magnitude of the generated measurement noise.

A higher noise density produces larger random fluctuations.

### 4.2 Sampling Frequency

The sampling frequency determines how frequently measurements are generated.

For a fixed noise density, increasing the sampling frequency increases the per-sample standard deviation according to the assumed bandwidth relationship.

For example, increasing the sampling frequency from 100 Hz to 400 Hz doubles the per-sample standard deviation under this model.

### 4.3 Random Seed

The random seed initializes NumPy's random-number generator.

Using the same seed and identical parameters produces the same sequence of noise samples.

Different seeds produce different deterministic sequences for the tested configurations.

The implementation uses `numpy.random.default_rng()` to maintain an independent random-number generator rather than modifying NumPy's global random state.

## 5. Implementation Architecture

The implementation is located in:

`sim/noise.py`

The class is named:

`WhiteNoiseGenerator`

Its responsibilities are:

1. Validate the supplied noise density and sampling frequency.
2. Initialize an independent random-number generator.
3. Calculate the discrete sample standard deviation.
4. Generate one Gaussian noise sample whenever `sample()` is called.

The standard deviation is calculated once during object initialization because the noise density and sampling frequency remain constant for a given generator instance.

The `sample()` method then generates a random value using a zero mean and the stored standard deviation.

The generator does not maintain a bias state or introduce temporal correlation between samples.

## 6. Verification and Testing

Automated tests are implemented in:

`tests/test_noise.py`

The component is verified using the following tests.

### 6.1 Reproducibility

Two generators initialized with identical parameters and random seeds should produce identical sequences.

This verifies deterministic behavior for repeatable simulation experiments.

### 6.2 Different Seeds

Generators initialized with different seeds are checked to ensure that the tested sequences differ.

This verifies the expected seed-dependent behavior, but does not establish statistical independence.

### 6.3 Mean and Standard Deviation

A large sequence of generated noise samples is evaluated statistically.

The sample mean is compared with the theoretical mean of zero.

The sample standard deviation is compared with the theoretical value:

$\sigma_n = N_g\sqrt{\frac{f_s}{2}}$

This checks whether the generated samples are statistically consistent with the intended Gaussian distribution.

### 6.4 Temporal Uncorrelation

The correlation between consecutive samples is calculated using the Pearson correlation coefficient.

The theoretical lag-one correlation for ideal white noise is:

$\rho_1 = 0$

The measured correlation is expected to remain close to zero within a finite-sample tolerance.

### 6.5 Parameter Validation

The constructor is tested against invalid parameter values.

The expected behavior is:

| Condition | Expected behavior |
|---|---|
| Negative noise density | Raise `ValueError` |
| Zero noise density | Accepted; generated samples are zero |
| Negative sampling frequency | Raise `ValueError` |
| Zero sampling frequency | Raise `ValueError` |
| NaN noise density | Raise `ValueError` |
| Infinite sampling frequency | Raise `ValueError` |

### 6.6 Current Test Results

The current automated test suite contains seven tests.

All seven tests passed in the latest reported run.

These results verify the tested implementation behavior. They do not establish that the model matches the noise characteristics of a particular physical gyroscope.

## 7. Integration with the Gyroscope Measurement Model

The white-noise generator is intended to be combined with the Gauss-Markov bias generator.

The complete simulated gyroscope measurement is represented as:

$\omega_m = \omega_{\text{true}} + b + n$

Where:

- $\omega_m$ is the measured angular velocity.
- $\omega_{\text{true}}$ is the true angular velocity.
- $b$ is the slowly varying gyroscope bias.
- $n$ is the white measurement noise.

The two stochastic components are generated independently.

This architecture allows the simulation to evaluate the effects of bias and measurement noise separately, as well as their combined effect on attitude estimation.

## 8. Assumptions and Limitations

This implementation uses a simplified white Gaussian measurement-noise model.

The following assumptions apply:

- Noise samples are Gaussian distributed.
- Noise samples are independent across discrete time steps.
- The noise mean is zero.
- Noise density remains constant during a simulation.
- Sampling frequency remains constant during a generator instance's lifetime.
- The effective noise bandwidth is approximated using the Nyquist frequency.
- The noise-density convention is treated as one-sided.

Real gyroscope behavior may differ because of analog filtering, digital filtering, sensor bandwidth limitations, internal signal processing, and datasheet noise-density conventions.

In particular, the conversion from noise density to discrete sample standard deviation is not universal for every sensor configuration. The actual effective bandwidth and filtering assumptions must be considered when using real sensor specifications.

This model does not independently simulate:

- Slowly varying gyroscope bias.
- Scale-factor errors.
- Axis misalignment.
- Temperature-dependent effects.
- Quantization noise.
- Saturation.
- Vibration sensitivity.
- Sensor-specific frequency-dependent noise.

The noise-density value currently used in the project is provisional and has not been fitted to measured sensor data.

## 9. Engineering Scope

The `WhiteNoiseGenerator` is a simulation and verification component intended to support estimator robustness testing.

It is not a complete physical gyroscope model and is not a certified flight-safety component.

Its purpose is to provide a controlled, reproducible source of Gaussian measurement noise that can be integrated into the broader UAV IMU simulation.