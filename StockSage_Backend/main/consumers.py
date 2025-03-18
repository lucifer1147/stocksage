import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .ProjectFiles.train import train

class TrainingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        params = data.get("params", {})

        # Define an async function to send updates
        async def send_update(message):
            await self.send(text_data=json.dumps(message))

        # Wrap the synchronous function `train()` into an async task
        loop = asyncio.get_event_loop()

        def run_training():
            """Runs the training process synchronously while sending live updates."""
            def callback(message):
                # Schedule the async send_update function in the event loop
                asyncio.run_coroutine_threadsafe(send_update(message), loop)

            train(callback=callback, **params)

        # Run the training function in a separate thread
        await sync_to_async(run_training, thread_sensitive=True)()

    async def disconnect(self, close_code):
        pass
