# train.py
import time

def train(epochs=10, learning_rate=0.001, callback=None):
    for epoch in range(1, epochs + 1):
        # Simulate training delay
        time.sleep(1)

        # Dummy loss calculation (replace with real model logic)
        loss = round(1 / (epoch * learning_rate), 4)

        # Send verbose message through callback
        if callback:
            callback({
                "epoch": epoch,
                "loss": loss,
                "message": f"Epoch {epoch}/{epochs} completed with loss: {loss}"
            })

    # Final message after training completion
    if callback:
        callback({"message": "Training complete!"})
