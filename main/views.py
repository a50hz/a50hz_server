from django.shortcuts import render
from django.http import HttpResponse
from .models import Measurement, Plot, Extent
from script import set_plot, get_processed_data, prepare_table
from datetime import datetime
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
        extent = Extent.objects.get(lat1 = data['lat1'], lat2 = data['lat2'], lng1 = data['lng1'], lng2 = data['lng2'])
        plot = Plot.objects.get(type=data.type, interpolation_type=data.method, extent_id=extent.id)
    return HttpResponse(plot.value)


def update(request):
    if request.method == 'POST':
        check = json.loads(request.body)
        if check['login'] == 'creator' and check['password'] == '11&(&*zD7K5TpJlZ':
            for extent in Extent.objects.all():
                coordinates = [extent.lat1, extent.lat2, extent.lng1, extent.lng2]
                coordinates = map(float, coordinates)
                lon_array, lat_array, point_grid = prepare_table(*coordinates)
                for method in ['griddata', 'spline', 'pandas']:
                    data = get_processed_data(lon_array, lat_array, point_grid, method)
                    for type in ['isolines', 'heatmap']:
                        plot = set_plot(data, type)
                        result = Plot(value=plot, type=type, interpolation_type=method, Extent=extent)
                        result.save()
        else:
            return HttpResponse("<h4>get of my site bitch</h4>")
    return HttpResponse("<h4>New plots built</h4>")                 


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