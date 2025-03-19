from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

from django.http import JsonResponse
from celery.result import AsyncResult
from django.core.cache import cache
from .dummyTrain import train_model

from .ProjectFiles.utils import STOCK

def start_training(request):
    """Start training and return task ID."""
    params = {}  # Modify this based on frontend input
    task = train_model.apply_async(args=[params])
    return JsonResponse({"task_id": task.id})

def get_training_status(request, task_id):
    """Fetch training progress and messages."""
    task_result = AsyncResult(task_id)
    response = {"status": task_result.status}

    # Fetch cached messages
    messages = cache.get(task_id, [])

    if task_result.status == "PROGRESS":
        response["progress"] = task_result.info.get("progress", 0)
        response["messages"] = messages

    elif task_result.status == "SUCCESS":
        response["result"] = task_result.result
        response["messages"] = messages

    return JsonResponse(response)

def get_data(request, ticker):
    data = STOCK(ticker=ticker.upper(), period='max')
    data.reset_index(inplace=True)
    
    response = {}
    for i in range(data.shape[0]):
        response[i] = data.iloc[i].to_dict()
    
    return JsonResponse({'response':response})

# Create your views here.
