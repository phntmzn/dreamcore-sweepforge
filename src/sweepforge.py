import os
import numpy as np
import soundfile as sf

# === CONFIG ===
sr = 48000
base_duration = 66.0          # 1 min 06 sec
f_min = 3000.0
f_max = 5000.0
num_sweeps = 100
out_dir = "PHNTMZN - DReAMCORE"

# Sweep variety controls
lfo_hz_min = 0.05             # slow sweep
lfo_hz_max = 2.00             # faster sweep
amp_min = 0.20
amp_max = 0.80

# Output gain
gain_db = 6.0
lin_gain = 10 ** (gain_db / 20.0)
peak_limit = 0.999  # prevent clipping

# Deterministic uniqueness (change seed if you want a different set)
rng = np.random.default_rng(1337)

os.makedirs(out_dir, exist_ok=True)

n = int(sr * base_duration)
t = np.arange(n, dtype=np.float64) / sr

for i in range(num_sweeps):
    # Unique per-file parameters
    lfo_hz = float(rng.uniform(lfo_hz_min, lfo_hz_max))
    lfo_phase = float(rng.uniform(0.0, 2.0 * np.pi))
    amp = float(rng.uniform(amp_min, amp_max))

    # LFO in [-1, 1]
    lfo = np.sin(2.0 * np.pi * lfo_hz * t + lfo_phase)

    # Instantaneous frequency oscillating between f_min and f_max
    f_inst = (f_min + f_max) / 2.0 + (f_max - f_min) / 2.0 * lfo

    # Integrate frequency to phase (FM synthesis style)
    phase = 2.0 * np.pi * np.cumsum(f_inst) / sr

    x = (amp * np.sin(phase))

    # Apply +6 dB gain (linear) and prevent clipping
    x *= lin_gain
    maxabs = float(np.max(np.abs(x)))
    if maxabs > peak_limit:
        x *= (peak_limit / maxabs)

    x = x.astype(np.float32)

    out_path = os.path.join(out_dir, f"PHNTMZN - DReAMCORE - {i:02d}.wav")
    sf.write(out_path, x, sr)

print(f"Wrote {num_sweeps} unique sweeps to: {out_dir}")
