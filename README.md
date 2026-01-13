# PHNTMZN – DReAMCORE SweepForge

Generate a folder of **100 unique sine sweeps** that **oscillate between 3000 Hz and 5000 Hz** and render as **48 kHz WAV** files. Each file is **1:06** long, has **+6 dB gain**, and is **peak-limited** to avoid clipping.

This repo is a simple Python batch renderer for creating consistent tone sweep source material for sound design, resampling, and composition workflows.

---

## What it makes

- Output folder: `PHNTMZN - DReAMCORE/`
- Files:
  - `PHNTMZN - DReAMCORE - 00.wav`
  - `PHNTMZN - DReAMCORE - 01.wav`
  - …
  - `PHNTMZN - DReAMCORE - 99.wav`

Each render varies by:
- LFO sweep speed (`lfo_hz`)
- LFO start phase (`lfo_phase`)
- Base amplitude (`amp`)

---

## Requirements

- Python 3.9+ recommended
- Packages:
  - `numpy`
  - `soundfile` (libsndfile)

---

## Install

```bash
pip install numpy soundfile
```

If `soundfile` fails to install on macOS, install `libsndfile`:

```bash
brew install libsndfile
```

---

## Usage

Run:

```bash
python sweepforge.py
```

After it finishes, you’ll have your WAVs in:

```text
PHNTMZN - DReAMCORE/
```

---

## Configuration

Edit these values in `sss.py`:

```python
sr = 48000
base_duration = 66.0
f_min = 3000.0
f_max = 5000.0
num_sweeps = 100
out_dir = "PHNTMZN - DReAMCORE"

lfo_hz_min = 0.05
lfo_hz_max = 2.00
amp_min = 0.20
amp_max = 0.80

gain_db = 6.0
peak_limit = 0.999

rng = np.random.default_rng(1337)
```

Notes:
- `gain_db = 6.0` applies a +6 dB boost (linear gain) before limiting.
- `peak_limit` rescales audio if a file would clip.
- Change the RNG seed to generate a different set of 100 files.

---

## How it works

For each file:
1. Create an LFO (`sin`) that swings between -1 and 1.
2. Map that to an instantaneous frequency between `f_min` and `f_max`.
3. Integrate frequency into phase (`cumsum`) to produce a smooth sweep oscillator.
4. Apply gain, then peak-safe limiting.
5. Export float32 WAV at `sr`.

---

## Quick ideas / extensions

- Add fade in/out (remove clicks)
- Randomize `f_min/f_max` per file (wider variety)
- Write stereo variants (phase offset or dual LFO)
- Export a CSV of per-file parameters
- Add CLI flags: `--count`, `--dur`, `--minhz`, `--maxhz`, `--gain-db`, `--seed`

---

## License

Choose a license that matches how you want others to use it (MIT is common for tools).
