"""
compare_models.py
-----------------
Train and compare 4 architectures on the same train/val/test split:
    CNN-LSTM  |  LSTM  |  BiLSTM  |  Transformer

Outputs (in outputs/):
    comparison_results.json     all metrics + loss histories + test predictions
    model_comparison.png        RMSE / MAE bar chart
    <Model>_prediction.png      per-model predicted vs actual
    <Model>/best_model.pt       per-model checkpoint
    features_cache.npz          cached features (skip raw reload on re-runs)

Usage:
    python compare_models.py
    python compare_models.py --epochs 50 --no-cache
"""

import sys
import os
import json
import time
import argparse

import torch
import numpy as np

# Critical Rules: ASCII/English ONLY for print statements, use Agg for matplotlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # ให้ import src/ และ report/ ได้

from src.paths import OUTPUT_DIR, FEATURES_CACHE, resolve_data_dir
from src.data_loader import load_dataset, compute_health_index
from src.features import extract_features
from src.dataset import split_dataset
from src.model import CNNLSTM
from src.models_extra import PureLSTM, BiLSTM, TransformerModel
from src.train import train

CACHE_PATH = FEATURES_CACHE

# Must match page1.html / main.py
WINDOW_SIZE = 20
HI_WINDOW = 7
N_FEATURES = 56
SEED = 42


def get_features(use_cache=True):
    """Load features from cache, or extract from raw IMS files and cache them."""
    if use_cache and CACHE_PATH.exists():
        print(f"Loading cached features from {CACHE_PATH} ...")
        cached = np.load(CACHE_PATH)
        return cached["features"]

    data_dir = resolve_data_dir()

    print("Loading raw data (this takes a few minutes)...")
    metadata, raw_data = load_dataset(data_dir, verbose=True)

    print("Extracting features...")
    features = extract_features(raw_data, fs=20000, verbose=True)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(CACHE_PATH, features=features)
    print(f"Cached features -> {CACHE_PATH}")
    return features


def main():
    parser = argparse.ArgumentParser(description="Compare RUL model architectures")
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--patience", type=int, default=15)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=5e-4)
    parser.add_argument("--no-cache", dest="use_cache", action="store_false")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    features = get_features(use_cache=args.use_cache)
    print(f"Features shape: {features.shape}")

    print("Computing health index labels...")
    rul_labels = compute_health_index(features, window=HI_WINDOW)

    print("Splitting dataset...")
    train_loader, val_loader, test_loader, scaler = split_dataset(
        features, rul_labels,
        window_size=WINDOW_SIZE,
        batch_size=args.batch_size,
        shuffle_split=True,
        random_seed=SEED,
    )

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    def build(name):
        """Fresh model with identical seed so every arch starts from the same RNG state."""
        torch.manual_seed(SEED)
        return {
            "CNN-LSTM":    lambda: CNNLSTM(n_features=N_FEATURES, window_size=WINDOW_SIZE),
            "LSTM":        lambda: PureLSTM(n_features=N_FEATURES, window_size=WINDOW_SIZE),
            "BiLSTM":      lambda: BiLSTM(n_features=N_FEATURES, window_size=WINDOW_SIZE),
            "Transformer": lambda: TransformerModel(n_features=N_FEATURES, window_size=WINDOW_SIZE),
        }[name]()

    model_names = ["CNN-LSTM", "LSTM", "BiLSTM", "Transformer"]
    results = {}

    for name in model_names:
        print(f"\n--- Training {name} ---")
        model = build(name).to(device)
        params = model.count_parameters()
        print(f"Parameters: {params:,}")

        # Model-specific output dir so checkpoints don't overwrite each other
        model_out_dir = OUTPUT_DIR / name
        model_out_dir.mkdir(parents=True, exist_ok=True)

        t0 = time.time()
        history = train(
            model=model,
            train_loader=train_loader,
            val_loader=val_loader,
            test_loader=test_loader,
            n_epochs=args.epochs,
            patience=args.patience,
            lr=args.lr,
            device=device,
            output_dir=str(model_out_dir),
        )
        train_time = time.time() - t0

        epochs_trained = len(history["train_loss"])

        results[name] = {
            "rmse": history["test_metrics"]["RMSE"],
            "mae": history["test_metrics"]["MAE"],
            "pearson_r": history["test_metrics"]["Pearson_r"],
            "params": params,
            "epochs_trained": epochs_trained,
            "train_time_sec": round(train_time, 1),
            "sec_per_epoch": round(train_time / max(epochs_trained, 1), 2),
            "best_val_loss": float(min(history["val_loss"])),
            "train_loss_history": history["train_loss"],
            "val_loss_history": history["val_loss"],
            "test_preds": history["test_preds"].tolist(),
            "test_targets": history["test_targets"].tolist(),
        }

        # Per-model prediction plot
        plt.figure(figsize=(10, 4))
        plt.plot(history["test_targets"], label="Actual", color="green", linewidth=2)
        plt.plot(history["test_preds"], label="Predicted", color="orange",
                 linewidth=1.5, linestyle="--")
        plt.title(f"{name} Prediction on Test Set (RMSE: {results[name]['rmse']:.4f})")
        plt.xlabel("Sample")
        plt.ylabel("Health Index")
        plt.legend()
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / f"{name}_prediction.png", dpi=150)
        plt.close()

        # Write partial results after each model, so a crash later keeps earlier work
        with open(OUTPUT_DIR / "comparison_results.json", "w") as f:
            json.dump(results, f, indent=2)

    print("\nGenerating comparison bar chart...")
    names = list(results.keys())
    rmses = [results[n]["rmse"] for n in names]
    maes = [results[n]["mae"] for n in names]

    x = np.arange(len(names))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x - width / 2, rmses, width, label='RMSE', color='skyblue')
    ax.bar(x + width / 2, maes, width, label='MAE', color='lightcoral')

    for i, (r, m) in enumerate(zip(rmses, maes)):
        ax.text(i - width / 2, r, f"{r:.4f}", ha='center', va='bottom', fontsize=8)
        ax.text(i + width / 2, m, f"{m:.4f}", ha='center', va='bottom', fontsize=8)

    ax.set_ylabel('Error Score')
    ax.set_title('Model Comparison by RMSE and MAE (lower is better)')
    ax.set_xticks(x)
    ax.set_xticklabels(names)
    ax.legend()

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "model_comparison.png", dpi=150)
    plt.close()

    # Overlay of all model predictions vs ground truth
    plt.figure(figsize=(12, 5))
    plt.plot(results[names[0]]["test_targets"], label="Actual", color="black", linewidth=2.2)
    for n, c in zip(names, ["#4f8ef7", "#f97316", "#a78bfa", "#f472b6"]):
        plt.plot(results[n]["test_preds"], label=n, color=c, linewidth=1.2, alpha=0.85)
    plt.title("All Models -- Predicted vs Actual Health Index (Test Set)")
    plt.xlabel("Sample")
    plt.ylabel("Health Index")
    plt.legend(ncol=5, fontsize=9)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "all_models_prediction.png", dpi=150)
    plt.close()

    best = min(names, key=lambda n: results[n]["rmse"])
    print("\nFinal Metrics:")
    for n in names:
        r = results[n]
        print(f"{n:<12} RMSE={r['rmse']:.4f}  MAE={r['mae']:.4f}  "
              f"r={r['pearson_r']:.4f}  params={r['params']:,}  "
              f"epochs={r['epochs_trained']}  time={r['train_time_sec']}s")
    print(f"\nBest by RMSE: {best}")


if __name__ == "__main__":
    main()
