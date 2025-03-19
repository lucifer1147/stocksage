from django.urls import path
from . import views

urlpatterns = [
    path("train/start-training/", views.start_training, name="start_training"),
    path("train/status/<str:task_id>/", views.get_training_status, name="training_status"),
    path('get-data/<str:ticker>/', views.get_data),
]
