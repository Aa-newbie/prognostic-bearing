"""
features.py
-----------
Extract time-domain and frequency-domain features from vibration signals.

Features per channel (4 channels x features = feature vector):
  Time domain (10):
    RMS, Peak, Peak-to-Peak, Crest Factor, Kurtosis, Skewness,
    Shape Factor, Impulse Factor, Margin Factor, Std

  Frequency domain (4):
    Band Energy Low (0-2.5kHz), Band Energy Mid (2.5-7.5kHz),
    Band Energy High (7.5-10kHz), Spectral Centroid

  Total: 14 features x 4 channels = 56 features per timestep
"""

import numpy as np
from scipy import stats
from scipy.fft import rfft, rfftfreq


# -------- Time-domain features --------

def compute_rms(x: np.ndarray) -> float:
    return float(np.sqrt(np.mean(x ** 2)))

def compute_peak(x: np.ndarray) -> float:
    return float(np.max(np.abs(x)))

def compute_peak_to_peak(x: np.ndarray) -> float:
    return float(np.max(x) - np.min(x))

def compute_crest_factor(x: np.ndarray) -> float:
    rms = compute_rms(x)
    return float(compute_peak(x) / (rms + 1e-10))

def compute_kurtosis(x: np.ndarray) -> float:
    return float(stats.kurtosis(x, fisher=True))

def compute_skewness(x: np.ndarray) -> float:
    return float(stats.skew(x))

def compute_shape_factor(x: np.ndarray) -> float:
    rms = compute_rms(x)
    mean_abs = float(np.mean(np.abs(x)))
    return rms / (mean_abs + 1e-10)

def compute_impulse_factor(x: np.ndarray) -> float:
    mean_abs = float(np.mean(np.abs(x)))
    return compute_peak(x) / (mean_abs + 1e-10)

def compute_margin_factor(x: np.ndarray) -> float:
    sqrt_mean_abs = float(np.mean(np.sqrt(np.abs(x)))) ** 2
    return compute_peak(x) / (sqrt_mean_abs + 1e-10)

def compute_std(x: np.ndarray) -> float:
    return float(np.std(x))


# -------- Frequency-domain features --------

def compute_freq_features(x: np.ndarray, fs: int = 20000) -> dict:
    """
    Compute FFT-based features.

    Args:
        x:  1D signal (20480 samples)
        fs: sampling frequency (Hz)
    """
    N = len(x)
    freqs = rfftfreq(N, d=1.0 / fs)
    fft_mag = np.abs(rfft(x)) / N

    total_energy = np.sum(fft_mag ** 2) + 1e-10
    low_mask  = freqs < 2500
    mid_mask  = (freqs >= 2500) & (freqs < 7500)
    high_mask = freqs >= 7500

    e_low  = float(np.sum(fft_mag[low_mask]  ** 2) / total_energy)
    e_mid  = float(np.sum(fft_mag[mid_mask]  ** 2) / total_energy)
    e_high = float(np.sum(fft_mag[high_mask] ** 2) / total_energy)
    centroid = float(np.sum(freqs * fft_mag) / (np.sum(fft_mag) + 1e-10))

    return {
        "band_energy_low":   e_low,
        "band_energy_mid":   e_mid,
        "band_energy_high":  e_high,
        "spectral_centroid": centroid / fs,
    }


# -------- Per-channel feature vector --------

def extract_channel_features(x: np.ndarray, fs: int = 20000) -> np.ndarray:
    """
    Extract feature vector from 1 channel signal.

    Returns:
        np.ndarray shape (14,)
    """
    time_feats = np.array([
        compute_rms(x),
        compute_peak(x),
        compute_peak_to_peak(x),
        compute_crest_factor(x),
        compute_kurtosis(x),
        compute_skewness(x),
        compute_shape_factor(x),
        compute_impulse_factor(x),
        compute_margin_factor(x),
        compute_std(x),
    ], dtype=np.float32)

    freq_feats_dict = compute_freq_features(x, fs=fs)
    freq_feats = np.array(list(freq_feats_dict.values()), dtype=np.float32)

    return np.concatenate([time_feats, freq_feats])  # (14,)


# -------- Full feature extraction --------

def extract_features(
    raw_data: np.ndarray,
    fs: int = 20000,
    verbose: bool = True
) -> np.ndarray:
    """
    Extract feature matrix from all timesteps.

    Args:
        raw_data: np.ndarray shape (N, 20480, 4)
        fs:       sampling frequency
        verbose:  show progress

    Returns:
        features: np.ndarray shape (N, 56)
    """
    from tqdm import tqdm

    N, samples, n_channels = raw_data.shape
    n_feats = 14

    features = np.zeros((N, n_feats * n_channels), dtype=np.float32)

    iterator = tqdm(range(N), desc="Extracting features") if verbose else range(N)

    for i in iterator:
        feat_row = []
        for ch in range(n_channels):
            ch_feats = extract_channel_features(raw_data[i, :, ch], fs=fs)
            feat_row.append(ch_feats)
        features[i] = np.concatenate(feat_row)

    print(f"[Features] Feature matrix shape: {features.shape}")
    return features


FEATURE_NAMES = []
for ch_idx in range(1, 5):
    for name in [
        "rms", "peak", "peak2peak", "crest_factor",
        "kurtosis", "skewness", "shape_factor",
        "impulse_factor", "margin_factor", "std",
        "band_energy_low", "band_energy_mid", "band_energy_high",
        "spectral_centroid"
    ]:
        FEATURE_NAMES.append(f"B{ch_idx}_{name}")

