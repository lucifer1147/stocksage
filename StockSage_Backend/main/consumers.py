import json
import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer
from concurrent.futures import ThreadPoolExecutor

from .ProjectFiles.dummyTrain import train

executor = ThreadPoolExecutor(max_workers=1)

class TrainingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        params = data.get("params", {})
        
        loop = asyncio.get_event_loop()

        # Define a callback to send verbose messages
        async def send_update(message):
            await self.send(text_data=json.dumps(message))

        # Bridge the async callback to the sync training function
        def callback(message):
            # Schedule the message to be sent in the event loop
            import asyncio
            asyncio.run_coroutine_threadsafe(send_update(message), loop)
            
        # Offload the train function to a separate thread
        await loop.run_in_executor(executor, lambda: train(**params, callback=callback))

    async def disconnect(self, close_code):
        pass