
# :sparkles: __AI Integration__ :sparkles:

This is the actual project with the :sparkles: __AI Integration__ :sparkles:. The directory has the following files:

### `train.py`
It houses the code for the train function. The parameters/arguments for the function are as explained in the CLI Interface README. In brief, the model is based on [__LTSM RNN__](https://en.wikipedia.org/wiki/Long_short-term_memory) implemented using [__PyTorch__](https://pytorch.org/), that takes stock data (name ohlcv data) and predicts the next day's ohlcv.

When the training function is run, if the `saveModelAs` param is give a string for the _model name_ then, a directory `Models/<model-name>_files` is created. It will contain the `<model-name>.pth` and `<model-name>_train_config.json` files which will have the [`state_dict`](https://pytorch.org/tutorials/recipes/recipes/what_is_state_dict.html) of the trained model and the parameters given while training.

Along with it, if the `saveExtrasToFile` is set to `true`, then the `Models/<model-name>_files` directory will have the following additional files:
- `Models/<model-name>_files/Tensors/<input-and-target-tensors>.pth`
- `Models/<model-name>_files/Scalers/<input-and-target-scalers>.pth`
- `Models/<model-name>_files/Tickers/<ticker-data-for-the-various-tickers>.csv>`

If `logToFile` is set to `true` then an additional `Models/<model-name>_files/<model-name>_training.log>` is created.

If `checkpointsIter` is given an integer value, it saves the best model's checkpoint every `checkpointsIter` epochs in a `Models/<model-name>_files/Checkpoints/<model-name>_checkpoint_<epoch>.pth` file. \
(Or it can save a `Models/<model-name>_files/Checkpoints/<model-name>_checkpoint_<epoch>_early.pth` file if `forceCompleteEpochs` is `false`)

### `utils.py`

As the name suggests, it contains some utility functions used in the `train.py` such as:
- `stock` &rarr; Returns the  _Ticker_ [_DataFrame_](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html).
- `preprocess` &rarr; Adds the date, day, month, year columns to the _Ticker DataFrame_. It also adds some technical indicators (mentioned later in `indicators.py` section).
- `getInput` &rarr; Converts  _Ticker DataFrame_ to a [_PyTorch Tensor_](https://pytorch.org/docs/stable/tensors.html).
- `loadData` &rarr; Actually loads the _Ticker DataFrame_ and handles the logic for saving csv files.
- `prepareInput` &rarr; Combines the above functions to get the Ticker Data, add features, convert to a tensor, apply scaling using scalers, transform to the data to input and output shape, converts them to tensors and finally returns them.

### `predict.py`
[To Be Added]

### `indicators.py`

Contains functions for calculating various technical indicators such as:
- [Relative Strength Index](https://www.investopedia.com/terms/r/rsi.asp)
- [Exponential Moving Average](https://www.investopedia.com/terms/e/ema.asp)
- [Moving Average Convergence Divergence](https://www.investopedia.com/terms/m/macd.asp)
- [Stoatic Oscillator](https://www.investopedia.com/terms/s/stochasticoscillator.asp)

### `neuralnet.py`

Contains the model and dataset classes and two utility functions as follow:
- [`class Model(nn.Module)`](https://pytorch.org/docs/stable/generated/torch.nn.Module.html) &rarr; The LTSM Model. Has the following layers:
    - [`LTSM Layer`](https://pytorch.org/docs/stable/generated/torch.nn.LSTM.html)
    - [`Normalisation Layer`](https://pytorch.org/docs/stable/generated/torch.nn.LayerNorm.html)
    - [`Fully Connected Layer`](https://pytorch.org/docs/stable/generated/torch.nn.Linear.html)

- [`class StockDataset(Dataset)`](https://pytorch.org/docs/stable/data.html#torch.utils.data.Dataset) &rarr; Creates the a custom dataset from the data recieved from `prepareInput`. Helps in implementing training loops with [`DataLoader`](https://pytorch.org/docs/stable/data.html#torch.utils.data.Dataset) class as it is convienient to do so.
- `getDevice` &rarr; Returns the device to be used for training.
- `init_weights` &rarr; Implements [__Xavier Weights Initialization__](https://365datascience.com/tutorials/machine-learning-tutorials/what-is-xavier-initialization/) for better training.


