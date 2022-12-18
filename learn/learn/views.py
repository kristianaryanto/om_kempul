from multiprocessing import context
from turtle import heading
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from .forms import NameForm

# def index(request):
#     return HttpResponse("hello word")



def index(request):

    return render(request,'base.html',context)

