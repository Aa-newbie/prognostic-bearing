import torch
import torch.nn as nn
import math

class PureLSTM(nn.Module):
    def __init__(self, n_features=56, window_size=20):
        super(PureLSTM, self).__init__()
        self.lstm1 = nn.LSTM(input_size=n_features, hidden_size=128, batch_first=True)
        self.lstm2 = nn.LSTM(input_size=128, hidden_size=64, batch_first=True)
        self.fc1 = nn.Linear(64, 32)
        self.fc2 = nn.Linear(32, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # x: (batch, window, features)
        x, _ = self.lstm1(x)
        x, _ = self.lstm2(x)
        x = x[:, -1, :]  # last timestep
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return self.sigmoid(x).squeeze(-1)   # (B,) to match label shape

    def count_parameters(self):
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

class BiLSTM(nn.Module):
    def __init__(self, n_features=56, window_size=20):
        super(BiLSTM, self).__init__()
        self.lstm1 = nn.LSTM(input_size=n_features, hidden_size=64, bidirectional=True, batch_first=True)
        self.lstm2 = nn.LSTM(input_size=128, hidden_size=32, bidirectional=True, batch_first=True)
        self.fc1 = nn.Linear(64, 32)
        self.fc2 = nn.Linear(32, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x, _ = self.lstm1(x)
        x, _ = self.lstm2(x)
        x = x[:, -1, :]
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return self.sigmoid(x).squeeze(-1)   # (B,)

    def count_parameters(self):
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000):
        super(PositionalEncoding, self).__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)  # (1, max_len, d_model)
        self.register_buffer('pe', pe)

    def forward(self, x):
        # x: (batch, seq_len, d_model)
        x = x + self.pe[:, :x.size(1), :]
        return x

class TransformerModel(nn.Module):
    def __init__(self, n_features=56, window_size=20):
        super(TransformerModel, self).__init__()
        self.pos_encoder = PositionalEncoding(d_model=n_features)
        encoder_layer = nn.TransformerEncoderLayer(d_model=n_features, nhead=4, dim_feedforward=128, batch_first=True)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=2)
        self.fc1 = nn.Linear(n_features, 32)
        self.fc2 = nn.Linear(32, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.pos_encoder(x)
        x = self.transformer_encoder(x)
        x = x.mean(dim=1)  # mean pool
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return self.sigmoid(x).squeeze(-1)   # (B,)

    def count_parameters(self):
        return sum(p.numel() for p in self.parameters() if p.requires_grad)
