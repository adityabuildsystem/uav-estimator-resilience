import numpy as np

from sim.generate_imu_data import generate_imu_data


def test_imu_dataset_shapes():
    data = generate_imu_data(
        duration_s=2.0,
        sample_rate_hz=100.0,
    )

    assert data["time"].shape == (200,)
    assert data["gyro_measurements"].shape == (200, 3)
    assert data["accel_measurements"].shape == (200, 3)


def test_imu_dataset_is_finite():
    data = generate_imu_data(duration_s=2.0)

    assert np.all(np.isfinite(data["gyro_measurements"]))
    assert np.all(np.isfinite(data["accel_measurements"]))


def test_imu_reproducibility():
    data1 = generate_imu_data(duration_s=2.0, seed=42)
    data2 = generate_imu_data(duration_s=2.0, seed=42)

    np.testing.assert_array_equal(
        data1["gyro_measurements"],
        data2["gyro_measurements"],
    )

    np.testing.assert_array_equal(
        data1["accel_measurements"],
        data2["accel_measurements"],
    )


def test_imu_contains_sensor_noise():
    data = generate_imu_data(duration_s=2.0)

    assert not np.array_equal(
        data["gyro_measurements"],
        data["body_rates"],
    )

    assert not np.array_equal(
        data["accel_measurements"],
        data["specific_force"],
    )
