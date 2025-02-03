import json
import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer
from concurrent.futures import ThreadPoolExecutor

from .ProjectFiles.train import train

executor = ThreadPoolExecutor(max_workers=1)

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

class TrainingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.stop_training = False
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        params = data.get("params", {})
        params = PRESETS[params.get("preset", "sm")]
        
        loop = asyncio.get_event_loop()

        # Define a callback to send verbose messages
        async def send_update(message):
            await self.send(text_data=json.dumps(message))

        # Bridge the async callback to the sync training function
        def callback(message):
            # Schedule the message to be sent in the event loop
            import asyncio
            asyncio.run_coroutine_threadsafe(send_update(message), loop)
            
        def train_with_stop_signal():
            train(callback=callback, stopSignal=lambda: self.stop_training, **params)
            
        # Offload the train function to a separate thread
        await loop.run_in_executor(executor, train_with_stop_signal)

    async def disconnect(self, close_code):
        self.stop_training = True  # Trigger to stop the training
        pass