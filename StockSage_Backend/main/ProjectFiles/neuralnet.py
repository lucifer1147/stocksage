import torch
import torch.nn as nn
from torch.utils.data import Dataset

def getDevice():
    return torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class Model(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size, dropout_prob):
        super(Model, self).__init__()
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, 
                            num_layers=num_layers, batch_first=True, dropout=dropout_prob)
        self.layer_norm = nn.LayerNorm(hidden_size)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = out[:, -1, :]
        out = self.layer_norm(out)
        out = self.fc(out)
        return out

class StockDataset(Dataset):
    def __init__(self, inputs, targets):
        assert len(inputs) == len(targets), "Inputs and targets must have the same length"
        self.inputs = inputs
        self.targets = targets

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx):
        input_tensor = self.inputs[idx].clone().detach().float()
        target_tensor = self.targets[idx].clone().detach().float()
        return input_tensor, target_tensor

def init_weights(m):
    if isinstance(m, nn.Linear) or isinstance(m, nn.LSTM):
        for param in m.parameters():
            if param.dim() > 1:
                nn.init.xavier_uniform_(param)
            else:
                nn.init.zeros_(param)