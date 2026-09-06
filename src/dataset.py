"""
dataset.py
----------
PyTorch Dataset for RUL prediction using sliding window.

Windowing strategy:
- Sliding window of size `window_size` timesteps
- Each sample is a sequence of feature vectors
- Label is the RUL at the last timestep of the window
"""

import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import StandardScaler
from typing import Optional


class BearingRULDataset(Dataset):
    """
    Dataset for RUL prediction.

    Args:
        features : np.ndarray shape (N, F)  -- feature matrix for all timesteps
        rul_labels: np.ndarray shape (N,)   -- RUL labels [0,1]
        window_size: number of timesteps per sample
        stride:     sliding window stride
        scaler:     StandardScaler (if None, a new one will be fit)
        fit_scaler: if True, fit scaler on this data
    """

    def __init__(
        self,
        features: np.ndarray,
        rul_labels: np.ndarray,
        window_size: int = 30,
        stride: int = 1,
        scaler: Optional[StandardScaler] = None,
        fit_scaler: bool = True,
    ):
        self.window_size = window_size
        self.stride = stride

        if scaler is None:
            scaler = StandardScaler()
        if fit_scaler:
            features = scaler.fit_transform(features)
        else:
            features = scaler.transform(features)
        self.scaler = scaler

        self.features = features.astype(np.float32)
        self.labels = rul_labels.astype(np.float32)

        self.indices = list(range(0, len(features) - window_size + 1, stride))

    def __len__(self) -> int:
        return len(self.indices)

    def __getitem__(self, idx: int):
        start = self.indices[idx]
        end = start + self.window_size

        x = torch.tensor(self.features[start:end], dtype=torch.float32)  # (window, F)
        y = torch.tensor(self.labels[end - 1], dtype=torch.float32)       # scalar

        return x, y


def split_dataset(
    features: np.ndarray,
    rul_labels: np.ndarray,
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    window_size: int = 30,
    stride_train: int = 1,
    stride_eval: int = 1,
    batch_size: int = 32,
    shuffle_split: bool = False,
    random_seed: int = 42,
) -> tuple:
    """
    Split dataset into train / val / test and create DataLoaders.

    Args:
        features:      (N, F)
        rul_labels:    (N,)
        train_ratio:   fraction for training (default 70%)
        val_ratio:     fraction for validation (default 15%)
        window_size:   timesteps per sample
        stride_train:  stride for training
        stride_eval:   stride for val/test
        batch_size:    batch size
        shuffle_split: if True, randomly shuffle windows before splitting
                       (avoids train/test distribution shift from temporal split)
        random_seed:   seed for reproducibility

    Returns:
        (train_loader, val_loader, test_loader, scaler)
    """
    from sklearn.preprocessing import StandardScaler

    N = len(features)
    n_train = int(N * train_ratio)
    n_val   = int(N * val_ratio)

    # Build all windows first
    all_indices = list(range(0, N - window_size + 1, 1))  # stride=1 for full pool

    if shuffle_split:
        rng = np.random.default_rng(random_seed)
        rng.shuffle(all_indices)

    # Compute split sizes based on window count
    n_win = len(all_indices)
    n_train_win = int(n_win * train_ratio)
    n_val_win   = int(n_win * val_ratio)

    train_idx = all_indices[:n_train_win]
    val_idx   = all_indices[n_train_win: n_train_win + n_val_win]
    test_idx  = all_indices[n_train_win + n_val_win:]

    # Fit scaler ONLY on rows covered by training windows -> no leakage from val/test
    train_rows = np.unique(np.concatenate(
        [np.arange(s, s + window_size) for s in train_idx]
    )) if len(train_idx) > 0 else np.arange(N)

    scaler = StandardScaler()
    scaler.fit(features[train_rows])
    features_scaled = scaler.transform(features).astype(np.float32)
    print(f"[Dataset] Scaler fit on {len(train_rows)}/{N} timesteps (train windows only)")

    print(f"[Dataset] Total windows: {n_win} -> Train: {len(train_idx)} | Val: {len(val_idx)} | Test: {len(test_idx)}")

    class IndexedDataset(Dataset):
        def __init__(self, indices, stride=1):
            self.indices = indices[::stride]
        def __len__(self):
            return len(self.indices)
        def __getitem__(self, i):
            start = self.indices[i]
            x = torch.tensor(features_scaled[start: start + window_size], dtype=torch.float32)
            y = torch.tensor(rul_labels[start + window_size - 1], dtype=torch.float32)
            return x, y

    train_ds = IndexedDataset(train_idx, stride=1)
    val_ds   = IndexedDataset(val_idx,   stride=max(1, stride_eval))
    test_ds  = IndexedDataset(test_idx,  stride=max(1, stride_eval))

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True,  num_workers=0)
    val_loader   = DataLoader(val_ds,   batch_size=batch_size, shuffle=False, num_workers=0)
    test_loader  = DataLoader(test_ds,  batch_size=batch_size, shuffle=False, num_workers=0)

    print(f"[Dataset] After stride -- Train: {len(train_ds)} | Val: {len(val_ds)} | Test: {len(test_ds)} samples")

    return train_loader, val_loader, test_loader, scaler


