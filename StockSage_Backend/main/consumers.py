import json

from channels.generic.websocket import AsyncWebsocketConsumer
from .ProjectFiles.train import train

class TrainingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        params = data.get("params", {})

        # Define a callback to send verbose messages
        async def send_update(message):
            await self.send(text_data=json.dumps(message))

        # Bridge the async callback to the sync training function
        def callback(message):
            # Schedule the message to be sent in the event loop
            import asyncio
            asyncio.create_task(send_update(message))

        # Start training with the callback
        train(callback=callback, **params)

    async def disconnect(self, close_code):
        pass