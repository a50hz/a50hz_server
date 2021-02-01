from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .models import Measurement
import script
import json
import datetime

class obj:

# constructor
    def __init__(self, dict1):
        self.__dict__.update(dict1)

def index(request):
    return render(request, 'main/index.html')


def get_isolines(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data['method'] == "griddata":
            return HttpResponse(script.get_isolines_griddata(data['x1'], data['x2'], data['y1'], data['y2']))
        elif data['method'] == "spline":
            return HttpResponse(script.get_isolines_spline(data['x1'], data['x2'], data['y1'], data['y2']))
        elif data['method'] == "pandas":
            return HttpResponse(script.get_isolines_pandas(data['x1'], data['x2'], data['y1'], data['y2']))
    else:
        return HttpResponse("Я жду POST запрос!")

        
def get_heatmap(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        return HttpResponse(script.get_heatmap(data['x1'], data['x2'], data['y1'], data['y2']))


def about(request):
    return HttpResponse("<h4>Page about my vkr</h4>")


def style(request):
    return render(request, 'main/style.css', content_type="text/css")


def scripts(request):
    return render(request, 'main/scripts.js', content_type="text/javascript")


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