"""
train.py
--------
Training loop, evaluation, and visualization for CNN-LSTM RUL Prediction.
"""

import os
import time
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from sklearn.metrics import mean_absolute_error, mean_squared_error


# ─────────────────────────── Training ───────────────────────────

def train_epoch(
    model: nn.Module,
    loader: DataLoader,
    optimizer,
    criterion,
    device: str,
) -> float:
    """Train 1 epoch, return average loss."""
    model.train()
    total_loss = 0.0

    for x, y in loader:
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad()
        pred = model(x)
        loss = criterion(pred, y)
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        total_loss += loss.item() * len(x)

    return total_loss / len(loader.dataset)


@torch.no_grad()
def evaluate(
    model: nn.Module,
    loader: DataLoader,
    criterion,
    device: str,
) -> tuple:
    """
    Evaluate model.

    Returns:
        (avg_loss, predictions, targets)
    """
    model.eval()
    total_loss = 0.0
    preds_list, targets_list = [], []

    for x, y in loader:
        x, y = x.to(device), y.to(device)
        pred = model(x)
        loss = criterion(pred, y)
        total_loss += loss.item() * len(x)
        preds_list.append(pred.cpu().numpy())
        targets_list.append(y.cpu().numpy())

    preds = np.concatenate(preds_list)
    targets = np.concatenate(targets_list)
    avg_loss = total_loss / len(loader.dataset)

    return avg_loss, preds, targets


def compute_metrics(preds: np.ndarray, targets: np.ndarray) -> dict:
    """Compute evaluation metrics."""
    rmse = float(np.sqrt(mean_squared_error(targets, preds)))
    mae = float(mean_absolute_error(targets, preds))
    corr, _ = pearsonr(targets, preds)
    return {"RMSE": rmse, "MAE": mae, "Pearson_r": float(corr)}


# ─────────────────────────── Main training loop ───────────────────────────

def train(
    model: nn.Module,
    train_loader: DataLoader,
    val_loader: DataLoader,
    test_loader: DataLoader,
    n_epochs: int = 100,
    lr: float = 1e-3,
    weight_decay: float = 1e-4,
    patience: int = 15,
    device: str = "cpu",
    output_dir: str = "outputs",
) -> dict:
    """
    Full training loop with early stopping and LR scheduling.

    Returns:
        history dict with train_loss, val_loss, metrics
    """
    os.makedirs(output_dir, exist_ok=True)
    checkpoint_path = os.path.join(output_dir, "best_model.pt")

    criterion = nn.MSELoss()
    optimizer = AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
    scheduler = CosineAnnealingLR(optimizer, T_max=n_epochs, eta_min=1e-5)

    history = {
        "train_loss": [],
        "val_loss": [],
    }

    best_val_loss = float("inf")
    patience_counter = 0

    print(f"\n{'='*60}")
    print(f"  Training CNN-LSTM | {n_epochs} epochs | device={device}")
    print(f"{'='*60}")
    print(f"{'Epoch':>6} | {'Train Loss':>10} | {'Val Loss':>10} | {'LR':>8} | {'Time':>6}")
    print("-" * 60)

    for epoch in range(1, n_epochs + 1):
        t0 = time.time()

        train_loss = train_epoch(model, train_loader, optimizer, criterion, device)
        val_loss, val_preds, val_targets = evaluate(model, val_loader, criterion, device)

        scheduler.step()
        elapsed = time.time() - t0

        history["train_loss"].append(train_loss)
        history["val_loss"].append(val_loss)

        current_lr = scheduler.get_last_lr()[0]
        print(f"{epoch:>6} | {train_loss:>10.6f} | {val_loss:>10.6f} | {current_lr:>8.2e} | {elapsed:>5.1f}s")

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
            torch.save(model.state_dict(), checkpoint_path)
        else:
            patience_counter += 1

        if patience_counter >= patience:
            print(f"\n[Early Stop] Epoch {epoch} -- no improvement in {patience} epochs")
            break

    print(f"\n[Done] Training complete | Best val loss: {best_val_loss:.6f}")
    print(f"[Done] Checkpoint saved: {checkpoint_path}\n")

    # Load best model and evaluate on test set
    model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    _, test_preds, test_targets = evaluate(model, test_loader, criterion, device)
    test_metrics = compute_metrics(test_preds, test_targets)

    print("[Metrics] Test Set:")
    for k, v in test_metrics.items():
        print(f"   {k}: {v:.4f}")

    history["test_preds"] = test_preds
    history["test_targets"] = test_targets
    history["test_metrics"] = test_metrics

    return history


# ─────────────────────────── Visualization ───────────────────────────

def plot_training_curve(history: dict, output_dir: str = "outputs"):
    """Plot train/val loss curve."""
    plt.figure(figsize=(10, 4))
    plt.plot(history["train_loss"], label="Train Loss", color="#2196F3")
    plt.plot(history["val_loss"],   label="Val Loss",   color="#F44336")
    plt.xlabel("Epoch")
    plt.ylabel("MSE Loss")
    plt.title("Training & Validation Loss")
    plt.legend()
    plt.tight_layout()
    save_path = os.path.join(output_dir, "training_curve.png")
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"[Plot] Saved: {save_path}")


def plot_rul_prediction(history: dict, output_dir: str = "outputs"):
    """Plot predicted RUL vs actual RUL on test set."""
    preds   = history["test_preds"]
    targets = history["test_targets"]
    metrics = history["test_metrics"]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    ax = axes[0]
    ax.plot(targets, label="Actual RUL",    color="#4CAF50", linewidth=2)
    ax.plot(preds,   label="Predicted RUL", color="#FF9800", linewidth=1.5, linestyle="--")
    ax.set_xlabel("Test Sample Index")
    ax.set_ylabel("RUL (normalized)")
    ax.set_title("RUL Prediction -- Test Set")
    ax.legend()
    ax.text(
        0.05, 0.05,
        f"RMSE={metrics['RMSE']:.4f}\nMAE={metrics['MAE']:.4f}\nr={metrics['Pearson_r']:.4f}",
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="bottom",
        bbox=dict(boxstyle="round", alpha=0.1),
    )

    ax = axes[1]
    ax.scatter(targets, preds, alpha=0.5, s=15, color="#9C27B0")
    lim = [0, 1]
    ax.plot(lim, lim, "k--", linewidth=1, label="Perfect prediction")
    ax.set_xlabel("Actual RUL")
    ax.set_ylabel("Predicted RUL")
    ax.set_title("Scatter: Actual vs Predicted")
    ax.legend()

    plt.tight_layout()
    save_path = os.path.join(output_dir, "rul_prediction.png")
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"[Plot] Saved: {save_path}")


def plot_feature_rms(
    features: np.ndarray,
    labels: np.ndarray = None,
    output_dir: str = "outputs"
):
    """Plot RMS of all bearings over time + optional label overlay."""
    rms_indices = [0, 14, 28, 42]
    colors = ["#2196F3", "#4CAF50", "#F44336", "#FF9800"]

    if labels is not None:
        fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True)
        ax_rms = axes[0]
        ax_hi  = axes[1]
    else:
        fig, ax_rms = plt.subplots(figsize=(12, 4))

    for i, (idx, color) in enumerate(zip(rms_indices, colors)):
        ax_rms.plot(features[:, idx], label=f"Bearing {i+1}", color=color, linewidth=1)
    ax_rms.set_ylabel("RMS")
    ax_rms.set_title("RMS Degradation Trend -- All Bearings (IMS 2nd_test)")
    ax_rms.legend(loc="upper left")

    if labels is not None:
        ax_hi.plot(labels, color="#9C27B0", linewidth=2, label="Health Index / RUL")
        ax_hi.set_xlabel("Timestep (every 10 min)")
        ax_hi.set_ylabel("HI / RUL")
        ax_hi.set_title("Label: Health Index over time")
        ax_hi.legend()
    else:
        ax_rms.set_xlabel("Timestep (every 10 min)")

    plt.tight_layout()
    save_path = os.path.join(output_dir, "rms_trend.png")
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"[Plot] Saved: {save_path}")


