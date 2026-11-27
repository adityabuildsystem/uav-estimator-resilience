
import numpy as np


def generate_trajectory(duration_s=120.0, sample_rate_hz=100.0):

    if not np.isfinite(duration_s) or duration_s <= 0:
        raise ValueError("duration_s must be finite and positive")

    if not np.isfinite(sample_rate_hz) or sample_rate_hz <= 0:
        raise ValueError("sample_rate_hz must be finite and positive")

    dt = 1.0 / sample_rate_hz
    time = np.arange(0.0, duration_s, dt)

    # Smooth attitude trajectory
    roll = np.deg2rad(8.0) * np.sin(0.20 * time)
    pitch = np.deg2rad(5.0) * np.sin(0.13 * time)
    yaw = np.deg2rad(12.0) * np.sin(0.08 * time)

    # Analytic Euler-angle derivatives
    roll_dot = np.deg2rad(8.0) * 0.20 * np.cos(0.20 * time)
    pitch_dot = np.deg2rad(5.0) * 0.13 * np.cos(0.13 * time)
    yaw_dot = np.deg2rad(12.0) * 0.08 * np.cos(0.08 * time)

    # ZYX Euler rates -> body angular velocity
    p = roll_dot - yaw_dot * np.sin(pitch)
    q = pitch_dot * np.cos(roll) + yaw_dot * np.sin(roll) * np.cos(pitch)
    r = -pitch_dot * np.sin(roll) + yaw_dot * np.cos(roll) * np.cos(pitch)

    body_rates = np.column_stack((p, q, r))
    euler_angles = np.column_stack((roll, pitch, yaw))

    # Specific force for zero translational acceleration:
    # f_body = R_body_to_nav.T @ [0, 0, g]
    g = 9.81
    specific_force = np.empty((len(time), 3))

    for i, (phi, theta, psi) in enumerate(euler_angles):
        cphi, sphi = np.cos(phi), np.sin(phi)
        ctheta, stheta = np.cos(theta), np.sin(theta)
        cpsi, spsi = np.cos(psi), np.sin(psi)

        rotation_body_to_nav = np.array([
            [cpsi * ctheta,
             cpsi * stheta * sphi - spsi * cphi,
             cpsi * stheta * cphi + spsi * sphi],

            [spsi * ctheta,
             spsi * stheta * sphi + cpsi * cphi,
             spsi * stheta * cphi - cpsi * sphi],

            [-stheta,
             ctheta * sphi,
             ctheta * cphi]
        ])

        specific_force[i] = rotation_body_to_nav.T @ np.array([0.0, 0.0, g])

    return {
        "time": time,
        "euler_angles": euler_angles,
        "body_rates": body_rates,
        "specific_force": specific_force,
    }
