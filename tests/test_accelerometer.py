import numpy as np
import pytest

from sim.accelerometer import Accelerometer


def make_accelerometer(seed=42, bias_std=None, noise_density=0.02):
    if bias_std is None:
        bias_std = np.full(3, 0.0005)

    return Accelerometer(
        dt=0.01,
        tau=10.0,
        bias_std=bias_std,
        noise_density=noise_density,
        seed=seed
    )


def test_output_shape():
    accel = make_accelerometer()

    output = accel.sample([0.0, 0.0, 9.81])

    assert output.shape == (3,)


def test_invalid_input_shape():
    accel = make_accelerometer()

    with pytest.raises(ValueError):
        accel.sample([9.81, 0.0])


def test_non_finite_input():
    accel = make_accelerometer()

    with pytest.raises(ValueError):
        accel.sample([0.0, np.nan, 9.81])


def test_reproducibility():
    accel1 = make_accelerometer(seed=42)
    accel2 = make_accelerometer(seed=42)

    for _ in range(100):
        out1 = accel1.sample([0.0, 0.0, 9.81])
        out2 = accel2.sample([0.0, 0.0, 9.81])

        np.testing.assert_array_equal(out1, out2)


def test_ideal_sensor():
    accel = make_accelerometer(
        bias_std=np.zeros(3),
        noise_density=0.0
    )

    true_force = np.array([0.0, 0.0, 9.81])

    measured = accel.sample(true_force)

    np.testing.assert_allclose(measured, true_force)


def test_bias_contributes_to_measurement():
    accel = make_accelerometer(
        bias_std=np.full(3, 0.01),
        noise_density=0.0
    )

    measured = accel.sample([0.0, 0.0, 0.0])

    assert np.any(measured != 0.0)