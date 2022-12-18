from contextvars import Context
from django.shortcuts import render
from django.http import HttpResponse,HttpRequest
import requests as req
import json
import pandas as pd
from .models import post
# Create your views here.

def index(request):
    #query
    posts = post.objects.all()
    context = {
        "title": "dari view",
        "Posts": posts,
    }
    return render(request,'blog.html',context)



def recent(request):
    return HttpResponse("ini recent")

def sklear(request):
    base = "http://127.0.0.1:2000/predictsk"
    data = {
    "bedrooms": 1,
    "bathrooms": 2.1,
    "sqft_living": 3,
    "sqft_above": 4,
    "grade": 5,
    "floors": 6.1,
    "view": 7,
    "sqft_lot": 8,
    "condition": 19,
    "waterfront": 10,
    "zipcode": 11
    }

    result = req.post(base,json=data).text
    return HttpResponse(result)

    
def tensorflow(request):
    base = "http://127.0.0.1:1234/predicttensor"
    data = {
    "bedrooms": 1,
    "bathrooms": 2.1,
    "sqft_living": 3,
    "sqft_above": 4,
    "grade": 5,
    "floors": 6.1,
    "view": 7,
    "sqft_lot": 8,
    "condition": 19,
    "waterfront": 10,
    "zipcode": 11
    }

    result = req.post(base,json=data).text
    return HttpResponse(result)

def mloflow(request):
        
        a = ["bedrooms","bathrooms","sqft_living","sqft_above","grade",
            "floors","view",'sqft_lot','condition','waterfront','zipcode'] 
        b = [(1,2,3,4,5,6,7,8,9,10,111)]
        model_input = pd.DataFrame( data = b,columns=a)

        X_test_json = model_input.to_json(orient='split')


        endpoint = 'http://127.0.0.1:8888/invocations'
        headers = {"Content-type": "application/json; format=pandas-split"} 
        response = req.post(endpoint, 
                                json = json.loads(X_test_json) , 
                                headers=headers)

        y_pred = json.loads(response.text)
        return HttpResponse(y_pred)

def input(request):
    return render(request,'input.html')
