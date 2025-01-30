from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

from .ProjectFiles.utils import STOCK

def index(request):
    pass

def train(request):
    pass

def predict(request):
    pass

def get_data(request, ticker):
    data = STOCK(ticker=ticker.upper(), period='max')
    data.reset_index(inplace=True)
    
    response = {}
    for i in range(data.shape[0]):
        response[i] = data.iloc[i].to_dict()
    
    return JsonResponse({'response':response})

# Create your views here.
