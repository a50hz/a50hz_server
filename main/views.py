from django.shortcuts import render
from django.http import HttpResponse
from .models import Measurement, Plot, Extent
from script import set_plot, get_processed_data, prepare_table
from datetime import datetime as dt
import numpy as np
import json
import datetime

class obj:

# constructor
    def __init__(self, dict1):
        self.__dict__.update(dict1)


def index(request):
    return render(request, 'main/index.html')


def get_plot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        plot = Plot.objects.get(type=data['type'], interpolation_type=data['method'], Extent_id=1)
    return HttpResponse(plot.value)              


def marker(request):
    res = list(Measurement.objects.all().values('latitude','longitude','data'))
    for i in range(len(res)):
        res[i] = list(map(float, res[i].values()))
    return HttpResponse(json.dumps(res))


def about(request):
    return HttpResponse("<h4>Page about GeoMagScan</h4>")


def privacy(request):
    return render(request, 'main/privacy.txt')


def data(request):
    if request.method == 'POST':
        data = json.loads(request.body, object_hook=obj)
        date = datetime.datetime.fromtimestamp(data.timestamp/1000)
        loc = data.geolocation
        row = Measurement(data=data.value, date_time=date, 
            longitude=loc.longitude, latitude=loc.latitude)
        row.save()
        return HttpResponse("Чекай табличку, детка!")
    else:
        return HttpResponse("Я жду POST запрос!")


def best_data(request):
    if request.method == 'POST':
        data = json.loads(request.body, object_hook=obj)
        for i in data.measurements:
            date = datetime.datetime.fromtimestamp(i.timestamp/1000)
            loc = i.geolocation
            row = Measurement(data=data.value, date_time=date, 
                longitude=loc.longitude, latitude=loc.latitude)
            row.save()
        return HttpResponse("Чекай табличку, детка!")
    else:
        return HttpResponse("Я жду POST запрос!")