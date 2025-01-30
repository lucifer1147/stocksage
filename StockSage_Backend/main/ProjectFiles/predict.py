import os
import json
import torch
import pandas as pd
from .neuralnet import Model
from .utils import prepareInput, preprocess


curDir = os.path.dirname(__file__)

def addPredict(X: torch.Tensor, pred: torch.Tensor, scalerX, scalerY):
    X_ = scalerX.inverse_transform(X[0].cpu())

    pred = scalerY.inverse_transform(pred.cpu())
    pred = torch.cat((torch.Tensor(pred).reshape(-1, 1), torch.Tensor([(X_[-1, 5]+1)%5, (X_[-1, 6]+1)%12]).reshape(-1, 1)))
    
    X_ = torch.concat((torch.tensor(X_[:, :7]), pred.reshape(1, -1)), dim=0)
    
    print(pd.DataFrame(X_))
    

def predict(modelName: str, stockToPredict: str):
    with open(os.path.join(curDir, f'./Models/{modelName}_files/{modelName}_train_config.json'), 'r') as f:
        trainConfig = json.load(f)
        
    model = Model(input_size=trainConfig['inputSize'], hidden_size=trainConfig['hiddenSize'], num_layers=trainConfig['numLayers'], output_size=trainConfig['outputSize'], dropout_prob=trainConfig['dropoutProb'])
    model.load_state_dict(torch.load(os.path.join(curDir, f'./Models/{modelName}_files/{modelName}.pth')))

    model.eval()

    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(DEVICE)

    X, _, scalerX, scalerY = prepareInput([stockToPredict], features=trainConfig['features'], timeframe=trainConfig['timeFrame'], addFeatures=trainConfig['addFeatures'], returnScaler=True, loadScaler=modelName, saveToFile=False)
    X = X[-1].reshape(1, trainConfig['timeFrame'], trainConfig['inputSize'])

    X = torch.Tensor(X).to(DEVICE)
    with torch.no_grad():
        pred = model(X)

    addPredict(X, pred, scalerX, scalerY)
