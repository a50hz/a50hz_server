from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
import script
import json


def index(request):
    return render(request, 'main/index.html')


def data(request):
    if request.method == 'GET':
        return render(request, 'main/data.json')
    elif request.method == 'POST':
        data = json.loads(request.body)
        return HttpResponse([*data.items()])
    else:
        return HttpResponse("Я жду GET или POST запрос придурок!")

def get_data(request):
    return HttpResponse("asdasd")


def about(request):
    return HttpResponse("<h4>Page about my vkr</h4>")