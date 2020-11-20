from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .models import Measurement
import script
import json
from django.contrib.gis.geos import Point
import datetime

class obj:

# constructor
    def __init__(self, dict1):
        self.__dict__.update(dict1)

def index(request):
    return render(request, 'main/index.html')


def data(request):
    if request.method == 'GET':
        return HttpResponse(script.prepare_file())
    elif request.method == 'POST':
        data = json.loads(request.body, object_hook=obj)
        print(type(data))
        date = datetime.datetime.fromtimestamp(data.timestamp/1000).time()
        a = Point(data.geolocation.latitude, data.geolocation.longitude)
        row = Measurement(data=data.value, time=date, location=a)
        row.save()

        return HttpResponse("Чекай табличку, детка!")
    else:
        return HttpResponse("Я жду GET или POST запрос!")


def get_data(request):
    return HttpResponse("asdasd")


def get_res(request):
    data = Measurement.objects.all()
    print(data)
    a = Point(coords)
    return HttpResponse(data)


def about(request):
    return HttpResponse("<h4>Page about my vkr</h4>")