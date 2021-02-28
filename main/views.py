from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .models import Measurement, Plot
import datetime
import json

class obj:

# constructor
    def __init__(self, dict1):
        self.__dict__.update(dict1)


def index(request):
    return render(request, 'main/index.html')


def get_plot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        plot = Plot.objects.order_by('date').reverse().filter(type=data['type'], interpolation_type=data['method'], Extent_id=1)[:1]
        if plot:
            return HttpResponse(plot[0].value)
        else:
            return HttpResponseNotFound()        


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
        if hasattr(data, 'measurements'):
            for i in data.measurements:
                date = datetime.datetime.fromtimestamp(i.timestamp/1000)
                loc = i.geolocation
                row = Measurement(data=i.value, date_time=date, 
                    longitude=loc.longitude, latitude=loc.latitude)
                row.save()
            return HttpResponse("Добавлен лист новых измерений")
        else:
            date = datetime.datetime.fromtimestamp(data.timestamp/1000)
            loc = data.geolocation
            row = Measurement(data=data.value, date_time=date, 
                longitude=loc.longitude, latitude=loc.latitude)
            row.save()
            return HttpResponse("Добавлено новое измерение")
    else:
        return HttpResponse("Я жду POST запрос!")