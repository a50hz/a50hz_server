from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .models import Measurement, Plot, ResearchZone
import datetime
import json


class obj:

    # constructor
    def __init__(self, dict1):
        self.__dict__.update(dict1)


def index(request):
    return render(request, 'main/index.html')


def cooler_index(request):
    return render(request, 'main/cooler_index.html')


def get_plot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        plot = Plot.objects.order_by('date').reverse().filter(
            kind=data['type'], interpolation_type=data['method'], Extent_id=1)[:1]
        if plot:
            return HttpResponse(plot[0].value)
        else:
            return HttpResponseNotFound()


def zones(request):
    if request.method == 'GET':
        res = list(ResearchZone.objects.all().values('id', 'name', 'lat1', 'lng1', 'lat2', 'lng2'))
        for i in range(len(res)):
            for j in ['lat1', 'lng1', 'lat2', 'lng2']:
                res[i][j] = float(res[i][j])
            res[i]["status"] = 'from database'
        return HttpResponse(json.dumps(res))
    elif request.method == "POST":
        data = json.loads(request.body)
        for i in data:
            if type(i) is int:
                ResearchZone.objects.filter(id=i).delete()
            elif type(i) is dict:
                if i['status'] == 'created':
                    i.pop('status')
                    i.pop('id')
                    ResearchZone.objects.create(**i)
                elif i['status'] == 'modified':
                    entry = ResearchZone.objects.get(id=i['id'])
                    entry.lat1 = i['lat1']
                    entry.lng1 = i['lng1']
                    entry.lat2 = i['lat2']
                    entry.lng2 = i['lng2']
                    entry.save()
                else:
                    pass
            else:
                pass
        return HttpResponse("Изменения зон внесены в базу")


def zone(request):
    if request.method == 'POST':
        id = json.loads(request.body)['id']
        res = list(ResearchZone.objects.filter(id=id).values('name', 'lat1', 'lng1', 'lat2', 'lng2'))[0]
        for j in ['lat1', 'lng1', 'lat2', 'lng2']:
            res[j] = float(res[j])
        return HttpResponse(json.dumps(res))
    else:
        return HttpResponse("Некорректный запрос!")


def points(request):
    if request.method == 'POST':
        id = json.loads(request.body)['id']
        zone = list(ResearchZone.objects.filter(id=id).values('lat1', 'lng1', 'lat2', 'lng2'))[0]
        points = list(Measurement.objects.filter(longitude__gte=zone["lng1"], longitude__lte=zone["lng2"], latitude__gte=zone["lat1"], latitude__lte=zone["lat2"]).values('latitude', 'longitude'))
        for i in range(len(points)):
            points[i] = list(map(float, points[i].values()))
        return HttpResponse(json.dumps(points))
    else:
        return HttpResponse("Некорректный запрос!")


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
    elif request.method == 'GET':
        res = list(Measurement.objects.all().values('latitude', 'longitude','data'))
        for i in range(len(res)):
            res[i] = list(map(float, res[i].values()))
        return HttpResponse(json.dumps(res))
