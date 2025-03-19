from celery import shared_task
import time
import redis

# Initialize Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@shared_task(bind=True)
def train_model(self, epochs=10):
    """
    Dummy model training function that simulates training over multiple epochs.
    Progress is stored in Redis for tracking.
    """
    task_id = self.request.id
    redis_key = f"train_progress:{task_id}"
    
    for epoch in range(epochs):
        time.sleep(1)  # Simulating training time per epoch
        progress = int(((epoch + 1) / epochs) * 100)
        redis_client.set(redis_key, progress)
        
    redis_client.set(redis_key, 100)  # Ensure 100% completion
    return {"task_id": task_id, "status": "Training completed", "progress": 100}