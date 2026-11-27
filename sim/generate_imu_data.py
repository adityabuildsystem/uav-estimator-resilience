
import numpy as np

from sim.trajectory import generate_trajectory
from sim.gyro import Gyroscope
from sim.accelerometer import Accelerometer


def generate_imu_data(
    duration_s=120.0,
    sample_rate_hz=100.0,
    seed=42,
):
    trajectory = generate_trajectory(
        duration_s=duration_s,
        sample_rate_hz=sample_rate_hz,
    )

    dt = 1.0 / sample_rate_hz

    gyro = Gyroscope(
        dt=dt,
        tau=10.0,
        bias_std=np.full(3, 0.0005),
        noise_density=0.005,
        seed=seed,
    )

    accel = Accelerometer(
        dt=dt,
        tau=10.0,
        bias_std=np.full(3, 0.005),
        noise_density=0.02,
        seed=seed + 2,
    )

    n = len(trajectory["time"])
    gyro_measurements = np.empty((n, 3))
    accel_measurements = np.empty((n, 3))

    for i in range(n):
        gyro_measurements[i] = gyro.sample(
            trajectory["body_rates"][i]
        )

        accel_measurements[i] = accel.sample(
            trajectory["specific_force"][i]
        )

    return {
        **trajectory,
        "gyro_measurements": gyro_measurements,
        "accel_measurements": accel_measurements,
    }

if __name__ == "__main__":
    data = generate_imu_data()
    print(f"Generated {len(data['time'])} IMU samples.")
    print("Gyro shape:", data["gyro_measurements"].shape)
    print("Accel shape:", data["accel_measurements"].shape)
