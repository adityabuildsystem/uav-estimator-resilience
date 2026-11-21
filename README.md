# UAV Estimator Resilience Test Harness

A small tool that stress-tests a UAV attitude estimator. It feeds in IMU data (simulated or from a flight log), injects realistic sensor faults, runs an Extended Kalman Filter (EKF), and generates a **Resilience Report** showing which faults break the estimate, how quickly they are detected, and how well the system recovers.

> **Status:** work in progress. Sections marked *TODO* are filled in as each stage is built. No results are claimed until the plots exist.

---

## Why this exists

Flight software teams usually test estimators on healthy sensor data. Real sensors drift, drop out, freeze, and spike. This harness makes it cheap to ask: *"What happens to my attitude estimate when the gyro drifts for 10 seconds?"* and get a repeatable, plotted answer.

## What it does

1. **Simulates** a flight trajectory and a noisy IMU (or replays a real log).
2. **Estimates** attitude with an EKF.
3. **Injects** faults into the sensor stream (bias step, drift ramp, dropout, frozen output, spikes, noise inflation, scale-factor error).
4. **Detects** faults with a residual-based (innovation / chi-square) test.
5. **Measures** peak error, RMSE, time-to-detect, false-alarm rate, and recovery time.
6. **Reports** everything in one HTML file (PDF optional).

## Quick start

```bash
git clone <repo-url>
cd <repo>
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python run.py --config config.yaml --faults all --out report/
```

Open `report/index.html`.  *(TODO: confirm commands once `run.py` exists.)*

## Configuration

Everything is controlled by `config.yaml`: simulation settings, IMU noise model, which faults to run, detector thresholds, and report options. The noise values should come from your own Allan-variance analysis of a real sensor. See the comments in the file.

## Fault models

| Fault | What it represents | Main parameters |
|---|---|---|
| Bias step | Sudden constant offset (e.g. after a shock) | magnitude, start time |
| Drift ramp | Slowly growing offset (e.g. temperature drift) | ramp rate, start time |
| Dropout | Sensor stops updating | start time, duration |
| Frozen output | Sensor repeats the last value | start time, duration |
| Spikes | Random outliers | probability, magnitude |
| Noise inflation | Noise level suddenly increases | multiplier, start time |
| Scale-factor error | Gain error on the measurement | factor, start time |

## Metrics

- **Peak attitude error:** largest error during or after the fault (degrees)
- **RMSE:** error over the whole run, and over the fault window
- **Time-to-detect:** seconds from fault start to the detector flagging it
- **False-alarm rate:** detector triggers per hour on fault-free data
- **Recovery time:** seconds for the error to return below a threshold after the fault ends

## Project structure

```
sim/          trajectory and IMU simulation, log loaders
estimator/    EKF implementation
faults/       fault injection library
detector/     residual-based detection
metrics/      metric calculations
report/       HTML report templates and generator
tests/        pytest tests (fixed random seeds)
data/         sample data (check licences before adding real logs)
config.yaml   run configuration
run.py        command-line entry point
```

## Example results

*TODO: add one plot per fault type and a summary table after the first full run.*

## Validation

*TODO: describe how the EKF was checked (for example, against ground truth in simulation, and against a complementary filter baseline).*

## Limitations (please read)

- This is an **engineering analysis tool**, not a certified safety-critical product, and not a safety certification.
- Unless you supply your own estimator or logs, the harness tests a **reference EKF** with your sensor characteristics. That is a proxy for your real system.
- Simulated faults are simplified models of real failures.

## Roadmap

- [ ] Python EKF baseline and complementary-filter comparison
- [ ] Fault injection library with plots
- [ ] Detector, metrics, and false-alarm analysis
- [ ] Real-log replay and automatic report
- [ ] C++ port of the estimator
- [ ] PX4 SITL integration (replay logs through PX4's own estimator)

## Contact

Author: Aditya (adityabuildsystem)
Email: aditya.autonomy@gmail.com

## Licence

Released under MIT License.