"""
main.py
-------
Entry point for Bearing RUL Prediction Pipeline.

Usage:
    python main.py
    python main.py --epochs 100 --batch_size 32 --label health_index
    python main.py --label piecewise

Steps:
    1. Load data from data/2nd_test/2nd_test/
    2. Extract features (time + frequency domain)
    3. Compute RUL / Health Index labels
    4. Create DataLoaders (train/val/test) with shuffle split
    5. Build and train CNN-LSTM model
    6. Evaluate and plot results
"""

import os
import sys
import argparse
import numpy as np
import torch

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # ให้ import src/ และ report/ ได้

from src.paths import OUTPUT_DIR, resolve_data_dir
from src.data_loader import (
    load_dataset,
    compute_linear_rul,
    compute_piecewise_rul,
    compute_health_index,
)
from src.features import extract_features
from src.dataset import split_dataset
from src.model import build_model
from src.train import train, plot_training_curve, plot_rul_prediction, plot_feature_rms


# ─────────────────────────── Config ───────────────────────────

CONFIG = {
    # Data
    "data_dir":    None,   # None = ใช้ค่าจาก src/paths.py
    "output_dir":  str(OUTPUT_DIR),

    # Label strategy: "health_index" | "piecewise" | "linear"
    # health_index is recommended — it tracks actual bearing degradation
    "label":       "health_index",

    # Dataset
    "window_size":    20,    # timesteps per sample (20 x 10min = ~3 hours)
    "stride_eval":    1,
    "train_ratio":    0.70,
    "val_ratio":      0.15,
    "batch_size":     32,
    "shuffle_split":  True,  # random split avoids train/test distribution mismatch
    "random_seed":    42,

    # Model
    "n_features":   56,      # 14 features x 4 channels
    "cnn_channels": (32, 64),
    "lstm_hidden":  (64, 32),
    "fc_hidden":    16,
    "dropout":      0.4,     # higher dropout for regularization

    # Training
    "n_epochs":     150,
    "lr":           5e-4,
    "weight_decay": 1e-3,
    "patience":     20,

    # Device
    "device":       "cuda" if torch.cuda.is_available() else "cpu",
}


def main():
    parser = argparse.ArgumentParser(description="Bearing RUL Prediction")
    parser.add_argument("--data_dir",   type=str,   default=None,
                        help="โฟลเดอร์ข้อมูล IMS (ไม่ระบุ = ใช้ data/2nd_test/2nd_test)")
    parser.add_argument("--epochs",     type=int,   default=CONFIG["n_epochs"])
    parser.add_argument("--batch_size", type=int,   default=CONFIG["batch_size"])
    parser.add_argument(
        "--label", type=str, default=CONFIG["label"],
        choices=["health_index", "piecewise", "linear"],
        help="RUL label strategy"
    )
    args = parser.parse_args()

    CONFIG["data_dir"]   = args.data_dir or str(resolve_data_dir())
    CONFIG["n_epochs"]   = args.epochs
    CONFIG["batch_size"] = args.batch_size
    CONFIG["label"]      = args.label

    print("=" * 60)
    print("  Bearing RUL Prediction -- CNN-LSTM")
    print(f"  Device : {CONFIG['device']}")
    print(f"  Label  : {CONFIG['label']}")
    print("=" * 60)

    # Step 1: Load data
    data_dir = CONFIG["data_dir"]
    if not os.path.isdir(data_dir):
        print(f"\n[ERROR] Folder not found: {data_dir}")
        print("  Please extract 2nd_test.rar to data/2nd_test/")
        print("  Run: python extract_data.py")
        sys.exit(1)

    metadata, raw_data = load_dataset(data_dir, verbose=True)
    N = len(raw_data)

    # Step 2: Extract features
    features = extract_features(raw_data, fs=20000, verbose=True)

    # Step 3: Compute labels
    if CONFIG["label"] == "health_index":
        labels = compute_health_index(features, window=7)
    elif CONFIG["label"] == "piecewise":
        labels = compute_piecewise_rul(N, usable_life_ratio=0.75)
    else:  # linear
        labels = compute_linear_rul(N)

    print(f"[Label]  Strategy: {CONFIG['label']} | range [{labels.min():.4f}, {labels.max():.4f}]")

    # Step 4: Plot degradation trend
    os.makedirs(CONFIG["output_dir"], exist_ok=True)
    plot_feature_rms(features, labels, output_dir=CONFIG["output_dir"])

    # Step 5: Create DataLoaders
    train_loader, val_loader, test_loader, scaler = split_dataset(
        features, labels,
        train_ratio=CONFIG["train_ratio"],
        val_ratio=CONFIG["val_ratio"],
        window_size=CONFIG["window_size"],
        stride_eval=CONFIG["stride_eval"],
        batch_size=CONFIG["batch_size"],
        shuffle_split=CONFIG["shuffle_split"],
        random_seed=CONFIG["random_seed"],
    )

    # Step 6: Build model
    model = build_model(
        n_features=CONFIG["n_features"],
        window_size=CONFIG["window_size"],
        cnn_channels=CONFIG["cnn_channels"],
        lstm_hidden=CONFIG["lstm_hidden"],
        fc_hidden=CONFIG["fc_hidden"],
        dropout=CONFIG["dropout"],
        device=CONFIG["device"],
    )

    # Step 7: Train
    history = train(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        test_loader=test_loader,
        n_epochs=CONFIG["n_epochs"],
        lr=CONFIG["lr"],
        weight_decay=CONFIG["weight_decay"],
        patience=CONFIG["patience"],
        device=CONFIG["device"],
        output_dir=CONFIG["output_dir"],
    )

    # Step 8: Visualize
    plot_training_curve(history, output_dir=CONFIG["output_dir"])
    plot_rul_prediction(history,  output_dir=CONFIG["output_dir"])

    # Summary
    metrics = history["test_metrics"]
    print("\n" + "=" * 60)
    print("  Done!")
    print(f"  RMSE      : {metrics['RMSE']:.4f}")
    print(f"  MAE       : {metrics['MAE']:.4f}")
    print(f"  Pearson r : {metrics['Pearson_r']:.4f}")
    print(f"  Outputs   : {os.path.abspath(CONFIG['output_dir'])}/")
    print("=" * 60)


if __name__ == "__main__":
    main()

