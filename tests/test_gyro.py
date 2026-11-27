import numpy as np
import pytest

from sim.gyro import Gyroscope

def test_gyro_output_shape():
    gyro = Gyroscope(0.01, 10, np.full(3,0.0005),0.005,42)
    measured = gyro.sample(np.array([0.1,0.2,0.3]))

    assert measured.shape == (3,)

def test_gryo_rejects_invalid_shape():
    gyro = Gyroscope(0.01,10,np.full(3,0.0005),0.005,42)

    with pytest.raises(ValueError):
        gyro.sample(np.array([0.1,0.2]))

def test_gyro_reproducibility():
    bias_std = np.array([0.0005]*3)

    gyro1 = Gyroscope(0.01, 10, bias_std, 0.005, 42)
    gyro2 = Gyroscope(0.01, 10, bias_std, 0.005, 42)

    for _ in range(100):
        result1 = gyro1.sample(np.array([0.1, 0.2, 0.3]))
        result2 = gyro2.sample(np.array([0.1, 0.2, 0.3]))

        np.testing.assert_array_equal(result1, result2)

def test_gyro_measurement_equation():
    bias_std = np.zeros(3)
    
def test_gyro_measurement_changes_with_bias():
    gyro = Gyroscope(0.01,10,np.full(3,0.0005),0, 42)

    true_rate = np.zeros(3)
    measured = gyro.sample(true_rate)

    assert np.any(measured !=0)