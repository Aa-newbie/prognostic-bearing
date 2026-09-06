"""
model.py
--------
CNN-LSTM Hybrid สำหรับ Bearing RUL Prediction

Architecture:
    Input: (batch, window_size, n_features)
        ↓  permute → (batch, n_features, window_size)  [channel-first สำหรับ Conv1d]
    Conv1D Block 1: Conv1d(64, k=7) → BN → ReLU → MaxPool(2)
    Conv1D Block 2: Conv1d(128, k=5) → BN → ReLU → MaxPool(2)
        ↓  permute → (batch, seq_len', 128)           [กลับไปเป็น time-first สำหรับ LSTM]
    LSTM(128, bidirectional=False) → Dropout(0.3)
    LSTM(64)                       → Dropout(0.3)
    FC(32) → ReLU
    FC(1)  → Sigmoid                                  [output RUL ∈ (0,1)]
"""

import torch
import torch.nn as nn
from torch import Tensor


class ConvBlock(nn.Module):
    """Conv1d → BatchNorm → ReLU → MaxPool"""

    def __init__(self, in_ch: int, out_ch: int, kernel_size: int, pool_size: int = 2):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv1d(in_ch, out_ch, kernel_size=kernel_size, padding=kernel_size // 2),
            nn.BatchNorm1d(out_ch),
            nn.ReLU(),
            nn.MaxPool1d(pool_size),
        )

    def forward(self, x: Tensor) -> Tensor:
        return self.net(x)


class CNNLSTM(nn.Module):
    """
    CNN-LSTM hybrid สำหรับ bearing RUL prediction

    Args:
        n_features:  จำนวน features ต่อ timestep (default 56)
        window_size: จำนวน timestep ใน sliding window (default 30)
        cnn_channels: tuple ของจำนวน filter แต่ละ Conv block
        lstm_hidden:  tuple ของ hidden size แต่ละ LSTM layer
        fc_hidden:    hidden size ของ FC layer
        dropout:      dropout rate
    """

    def __init__(
        self,
        n_features: int = 56,
        window_size: int = 30,
        cnn_channels: tuple = (64, 128),
        lstm_hidden: tuple = (128, 64),
        fc_hidden: int = 32,
        dropout: float = 0.3,
    ):
        super().__init__()

        self.n_features = n_features
        self.window_size = window_size

        # --- CNN layers ---
        self.conv1 = ConvBlock(n_features, cnn_channels[0], kernel_size=7)
        self.conv2 = ConvBlock(cnn_channels[0], cnn_channels[1], kernel_size=5)

        # หลังผ่าน 2 MaxPool(2) → seq_len = window_size // 4
        cnn_out_len = window_size // 4

        # --- LSTM layers ---
        self.lstm1 = nn.LSTM(
            input_size=cnn_channels[1],
            hidden_size=lstm_hidden[0],
            batch_first=True,
        )
        self.dropout1 = nn.Dropout(dropout)

        self.lstm2 = nn.LSTM(
            input_size=lstm_hidden[0],
            hidden_size=lstm_hidden[1],
            batch_first=True,
        )
        self.dropout2 = nn.Dropout(dropout)

        # --- FC layers ---
        self.fc = nn.Sequential(
            nn.Linear(lstm_hidden[1], fc_hidden),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(fc_hidden, 1),
            nn.Sigmoid(),
        )

    def forward(self, x: Tensor) -> Tensor:
        """
        Args:
            x: (batch, window_size, n_features)

        Returns:
            rul: (batch,) — predicted RUL ∈ (0,1)
        """
        # Conv1d ต้องการ (batch, channels, seq_len)
        x = x.permute(0, 2, 1)             # → (B, F, W)

        x = self.conv1(x)                  # → (B, 64, W/2)
        x = self.conv2(x)                  # → (B, 128, W/4)

        # LSTM ต้องการ (batch, seq_len, features)
        x = x.permute(0, 2, 1)             # → (B, W/4, 128)

        x, _ = self.lstm1(x)               # → (B, W/4, 128)
        x = self.dropout1(x)

        x, _ = self.lstm2(x)               # → (B, W/4, 64)
        x = self.dropout2(x)

        # ใช้ output จาก timestep สุดท้าย
        x = x[:, -1, :]                    # → (B, 64)

        out = self.fc(x)                   # → (B, 1)
        return out.squeeze(-1)             # → (B,)

    def count_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


def build_model(
    n_features: int = 56,
    window_size: int = 30,
    cnn_channels: tuple = (64, 128),
    lstm_hidden: tuple = (128, 64),
    fc_hidden: int = 32,
    dropout: float = 0.3,
    device: str = "cpu",
) -> CNNLSTM:
    """Build and initialize model."""
    model = CNNLSTM(
        n_features=n_features,
        window_size=window_size,
        cnn_channels=cnn_channels,
        lstm_hidden=lstm_hidden,
        fc_hidden=fc_hidden,
        dropout=dropout,
    )
    model = model.to(device)
    print(f"[Model] CNN-LSTM | Parameters: {model.count_parameters():,} | Device: {device}")
    return model
