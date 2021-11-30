from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(req):
    return HttpResponse("Hello world, this is FSM-Football")
