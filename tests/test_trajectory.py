
import numpy as np
import pytest

from sim.trajectory import generate_trajectory


def test_trajectory_shapes():
    data = generate_trajectory(duration_s=2.0, sample_rate_hz=100.0)

    assert data["time"].shape == (200,)
    assert data["euler_angles"].shape == (200, 3)
    assert data["body_rates"].shape == (200, 3)
    assert data["specific_force"].shape == (200, 3)


def test_trajectory_is_finite():
    data = generate_trajectory()

    for values in data.values():
        assert np.all(np.isfinite(values))


def test_specific_force_magnitude():
    data = generate_trajectory()

    magnitudes = np.linalg.norm(data["specific_force"], axis=1)

    np.testing.assert_allclose(magnitudes, 9.81, atol=1e-10)


def test_invalid_duration():
    with pytest.raises(ValueError):
        generate_trajectory(duration_s=0)


def test_invalid_sample_rate():
    with pytest.raises(ValueError):
        generate_trajectory(sample_rate_hz=-100)
