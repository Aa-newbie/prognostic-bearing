"""
data_loader.py
--------------
Load and parse IMS Bearing Dataset files (2nd_test).

IMS 2nd_test format:
- Each file is named by timestamp e.g. "2004.02.12.10.32.39"
- ASCII tab-separated data
- 20,480 rows x 4 columns (Bearing 1-4)
- Sampling rate: 20,000 Hz (1 second per file)
- Recorded every 10 minutes
"""

import os
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
from tqdm import tqdm

# Recordings below this overall RMS are treated as "rig already stopped"
# rather than as a measurement of a bearing. See load_dataset().
MIN_RMS = 0.01


def parse_ims_filename(filename: str) -> datetime:
    """Parse IMS filename into datetime object."""
    parts = filename.strip().split(".")
    if len(parts) == 6:
        try:
            return datetime(
                int(parts[0]), int(parts[1]), int(parts[2]),
                int(parts[3]), int(parts[4]), int(parts[5])
            )
        except ValueError:
            return None
    return None


def load_single_file(filepath: str) -> np.ndarray:
    """
    Load a single IMS file.

    Returns:
        np.ndarray shape (20480, 4) -- 4 channels, 20480 samples
    """
    data = np.loadtxt(filepath)
    if data.ndim == 1:
        data = data.reshape(-1, 1)
    return data.astype(np.float32)


def load_dataset(data_dir: str, verbose: bool = True) -> tuple:
    """
    Load entire dataset from an IMS 2nd_test folder.

    Args:
        data_dir: path to folder containing IMS files (e.g. data/2nd_test/)
        verbose:  show progress bar

    Returns:
        metadata  : DataFrame with ['filename', 'timestamp', 'timestep']
        raw_data  : np.ndarray shape (N, 20480, 4)
    """
    data_dir = Path(data_dir)
    all_files = sorted(
        [f for f in data_dir.iterdir() if f.is_file()],
        key=lambda f: f.name
    )

    if len(all_files) == 0:
        raise FileNotFoundError(f"[DataLoader] No files found in {data_dir}")

    print(f"[DataLoader] Found {len(all_files)} files in {data_dir}")

    records = []
    data_list = []
    dropped_idle = []

    iterator = tqdm(all_files, desc="Loading files") if verbose else all_files

    for i, filepath in enumerate(iterator):
        ts = parse_ims_filename(filepath.name)
        try:
            arr = load_single_file(str(filepath))
        except Exception:
            continue  # skip broken files

        # Skip too-short files or headers
        if arr.shape[0] < 100:
            continue
        if arr.shape[1] < 4:
            arr = np.pad(arr, ((0, 0), (0, 4 - arr.shape[1])), mode='constant')

        arr = arr[:, :4]  # use only 4 channels

        # Skip recordings made while the rig was already stopped.
        # The last files of 2nd_test hold near-zero signal (RMS ~0.002 vs ~0.5
        # just before). They are not measurements of a bearing, and because
        # compute_health_index() normalises by column min/max they would
        # otherwise become the "healthiest" point in the whole run -- right at
        # the moment of failure.
        if float(np.sqrt(np.mean(arr ** 2))) < MIN_RMS:
            dropped_idle.append(filepath.name)
            continue

        records.append({
            "filename": filepath.name,
            "timestamp": ts,
            "timestep": i,
        })
        data_list.append(arr)

    metadata = pd.DataFrame(records)
    raw_data = np.stack(data_list, axis=0)  # (N, 20480, 4)

    if dropped_idle:
        print(f"[DataLoader] Dropped {len(dropped_idle)} idle recordings "
              f"(RMS < {MIN_RMS}): {', '.join(dropped_idle)}")

    print(f"[DataLoader] Loaded successfully -- shape: {raw_data.shape}")
    print(f"[DataLoader] Time range: {metadata['timestamp'].min()} -> {metadata['timestamp'].max()}")

    return metadata, raw_data


def compute_linear_rul(n_timesteps: int) -> np.ndarray:
    """
    Compute linearly decaying RUL labels (normalized).
    - timestep 0   -> RUL = 1.0 (healthy)
    - timestep N-1 -> RUL = 0.0 (failed)

    Returns:
        np.ndarray shape (N,) float32
    """
    return np.linspace(1.0, 0.0, n_timesteps, dtype=np.float32)


def compute_piecewise_rul(n_timesteps: int, usable_life_ratio: float = 0.8) -> np.ndarray:
    """
    Piecewise-linear RUL label:
    - Stage 1 (0 .. usable_life_ratio): RUL stays at 1.0  (healthy plateau)
    - Stage 2 (usable_life_ratio .. 1): linearly 1.0 -> 0.0  (degradation)

    This is more realistic than a pure linear label for bearings that
    run normally for most of their life before failing rapidly.

    Args:
        n_timesteps:      total number of time steps
        usable_life_ratio: fraction of life that stays at RUL=1.0 (default 0.8)

    Returns:
        np.ndarray shape (N,) float32
    """
    rul = np.ones(n_timesteps, dtype=np.float32)
    cutoff = int(n_timesteps * usable_life_ratio)
    rul[cutoff:] = np.linspace(1.0, 0.0, n_timesteps - cutoff, dtype=np.float32)
    return rul


def compute_health_index(features: np.ndarray, window: int = 5) -> np.ndarray:
    """
    Compute a Health Index (HI) from extracted features.

    Strategy:
    1. Compute a composite degradation score = mean of normalized
       {RMS, Kurtosis, Crest Factor} across all 4 channels.
    2. Smooth with rolling window to reduce noise.
    3. Normalize to [0, 1] range and INVERT so that:
       - HI = 1.0  at start  (healthy)
       - HI = 0.0  at end    (failed)

    This produces a data-driven label that tracks the actual
    bearing degradation rather than assuming linear decay.

    Args:
        features: np.ndarray shape (N, 56)  -- output of extract_features()
        window:   smoothing window (timesteps)

    Returns:
        hi: np.ndarray shape (N,) float32, values in [0, 1]
    """
    # Feature indices per channel:
    # B1: rms=0, crest=3, kurtosis=4
    # B2: rms=14, crest=17, kurtosis=18
    # B3: rms=28, crest=31, kurtosis=32
    # B4: rms=42, crest=45, kurtosis=46
    health_indices = {
        "rms":      [0, 14, 28, 42],
        "crest":    [3, 17, 31, 45],
        "kurtosis": [4, 18, 32, 46],
    }

    degradation_score = np.zeros(len(features), dtype=np.float64)

    for feat_name, idxs in health_indices.items():
        for idx in idxs:
            col = features[:, idx].astype(np.float64)
            col_min = col.min()
            col_max = col.max()
            if col_max - col_min > 1e-10:
                col_norm = (col - col_min) / (col_max - col_min)
            else:
                col_norm = np.zeros_like(col)
            degradation_score += col_norm

    degradation_score /= degradation_score.max() + 1e-10

    # Smooth to reduce noise
    import pandas as pd
    s = pd.Series(degradation_score)
    degradation_score = s.rolling(window=window, min_periods=1, center=True).mean().values

    # Invert: high degradation -> low health
    hi = 1.0 - degradation_score
    hi = np.clip(hi, 0.0, 1.0).astype(np.float32)

    print(f"[DataLoader] Health Index range: [{hi.min():.4f}, {hi.max():.4f}]")
    return hi

