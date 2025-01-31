from main.ProjectFiles.train import train
from main.ProjectFiles.predict import predict

import argparse
import datetime as dt

import datetime as dt

optimizers = ['adamw', 'adam', 'rmsprop']
schedulers = ['steplr', 'cosineannealinglr', 'reduceonplateau']

param_set_sm = {
    "tickers": ['NVDA', 'AAPL', 'MSFT', 'AMZN'],
    "numLayers": 5,
    "hiddenSize": 512,
    "learningRate": 0.001,
    "batchSize": 16,
    "dropoutProb": 0.2,
    "addFeatures": [],
    "timeFrame": 20,
    "saveExtrasToFile": True,
    "saveModelAs": "sm_stock_model",
    "checkpointsIter": 20,
    "maxEpochs": 50,
    "minEpochs": 10,
    "patience": 10,
    "plotLoss": True,
}

param_set_md = {
    "tickers": ['NVDA', 'AAPL', 'MSFT', 'AMZN'],
    "numLayers": 6,
    "hiddenSize": 1024,
    "learningRate": 0.0005,
    "batchSize": 16,
    "dropoutProb": 0.25,
    "addFeatures": ['rsi', 'ema'],
    "timeFrame": 30,
    "saveExtrasToFile": True,
    "saveModelAs": "md_stock_model",
    "checkpointsIter": 10,
    "maxEpochs": 100,
    "minEpochs": 10,
    "patience": 10,
    "plotLoss": True,
}

param_set_lg = {
    "tickers": ['NVDA', 'AAPL', 'MSFT', 'AMZN'],
    "numLayers": 8,
    "hiddenSize": 2048,
    "learningRate": 0.0001,
    "batchSize": 32,
    "dropoutProb": 0.3,
    "addFeatures": ['macd', 'rsi', 'ema', 'signal line'],
    "timeFrame": 45,
    "saveExtrasToFile": True,
    "saveModelAs": "lg_stock_model",
    "checkpointsIter": 5,
    "maxEpochs": 150,
    "minEpochs": 10,
    "patience": 10,
    "plotLoss": True,
}

param_set_xl = {
    "tickers": ['NVDA', 'AAPL', 'MSFT', 'AMZN'],
    "numLayers": 10,
    "hiddenSize": 4096,
    "learningRate": 0.00001,
    "batchSize": 64,
    "dropoutProb": 0.4,
    "addFeatures": ['macd', 'rsi', 'ema', 'signal line', 'fast%k', 'slow%d'],
    "timeFrame": 60,
    "saveExtrasToFile": True,
    "saveModelAs": "xl_stock_model",
    "checkpointsIter": 2,
    "maxEpochs": 200,
    "minEpochs": 10,
    "patience": 10,
    "plotLoss": True,
}

PRESETS = {
    'sm': param_set_sm,
    'md': param_set_md,
    'lg': param_set_lg,
    'xl': param_set_xl
}


def parse_args():
    parser = argparse.ArgumentParser(description="Stock Predictor CLI.")
    posCommand = parser.add_subparsers(dest="command")
    
    train_parser = posCommand.add_parser("train")
    test_parser = posCommand.add_parser("test")
    predict_parser = posCommand.add_parser("predict")

    train_parser.add_argument("-p", "--preset", choices=PRESETS.keys(), default="sm", help="Choose a preset configuration")

    train_parser.add_argument("--num_layers", type=int, help="Number of LSTM layers")
    train_parser.add_argument("--hidden_size", type=int, help="Size of hidden layers")
    train_parser.add_argument("--learning_rate", type=float, help="Learning rate")
    train_parser.add_argument("--batch_size", type=int, help="Batch size")
    train_parser.add_argument("--dropout_prob", type=float, help="Dropout probability")
    train_parser.add_argument("--max_epochs", type=int, help="Maximum number of training epochs")
    train_parser.add_argument("--min_epochs", type=int, help="Minimum number of training epochs")
    train_parser.add_argument("--patience", type=int, help="Patience for early stopping")

    train_parser.add_argument("--tickers", nargs="+", help="List of stock tickers")
    train_parser.add_argument("--add_features", nargs="+", help="Additional feature engineering options")
    train_parser.add_argument("--time_frame", type=int, help="Time frame for input data")

    train_parser.add_argument("--save_model_as", type=str, help="Filename for saving the trained model")
    train_parser.add_argument("--checkpoints_iter", type=int, help="Checkpoint saving interval")
    
    train_parser.add_argument("-s", "--save_extras_to_file", action="store_true", help="Save additional training data")
    train_parser.add_argument("-d", "--debug", action="store_true", help="Enable debugging mode")
    train_parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose")
    train_parser.add_argument("-l", "--log_to_file", action="store_true", help="Log to file")
    train_parser.add_argument("-f", "--force_complete_epochs", action="store_true", help="Force training to complete all epochs")
    train_parser.add_argument("-m", "--plot_loss", action="store_true", help="Plot loss during training")
    
    train_parser.add_argument("--optimizer_choice", choices=optimizers, type=str, help="Optimizer choice", default="adamw")
    train_parser.add_argument("--scheduler_choice", choices=schedulers, type=str, help="Scheduler choice", default="cosineannealinglr")

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    param_set = PRESETS[args.preset].copy()

    for key, value in vars(args).items():
        if value is not None and key != "preset" and key != "command":
            key = key.split('_')
            key[1:] = [s.capitalize() for s in key[1:]]
            key = ''.join(key)
            param_set[key] = value
    
    print(f'\nSelected command \'{args.command}\' using the following parameters:')
    for key, val in param_set.items():
        print(f'\t{key}: {val}')
    
    ans = str(input("\nStart training with the above parameters? (y/n): "))

    if ans != "y":
        quit()
        
    now = dt.datetime.now()    
    if args.command == "train":
        print(f"\nTraining started at {now}")
        train(**param_set)
        print(f"Training Completed! Took {str(dt.datetime.now() - now)}")
        