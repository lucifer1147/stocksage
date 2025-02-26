from django.urls import path
from .consumers import TrainingConsumer

websocket_urlpatterns = [
    path('ws/train/', TrainingConsumer.as_asgi()),
]