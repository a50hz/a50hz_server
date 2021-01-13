import numpy as np
import matplotlib.pyplot as plt
import geojsoncontour
import math
from django.db import connection
from main.models import Measurement


def aget_isolines(x1, x2, y1, y2):
    step = max((x1-x2)/1000, (y1-y2)/1000)
    data = get_data(x1, x2, y1, y2, step)
    lon_range, lat_range = np.mgrid[x2:x1:step, y2:y1:step] # 6 знаков после запятой
    Z = np.sinc(lon_range) * np.cos(lat_range)
    figure = plt.figure()
    ax = figure.add_subplot(111)
    contour = ax.contour(lon_range, lat_range, Z, levels=16)
    geojson = geojsoncontour.contour_to_geojson(
        contour=contour,
        ndigits=3,
        unit='m'
    )
    return geojson


def get_isolines(x1, x2, y1, y2, zoom):
    #data =  my_custom_sql("SELECT * FROM public.main_measurement WHERE ({} < longitude) and (longitude < {}) and ({} < latitude) and (latitude < {})".format((lon_array[i]-step), (lon_array[i]+step), (lat_array[j]-step), (lat_array[j]+step)))
    step = max((x1-x2)/(100*2**(19/zoom+1)), (y1-y2)/(100*2**(19/zoom+1)))
    lon_array = [i for i in np.arange(x2,x1,step)] #ширина
    lat_array = [i for i in np.arange(y2,y1,step)] #высота

    data = get_data(x1, x2, y1, y2, step)
    point_grid = np.zeros(
        (len(lat_array), len(lon_array))
    )

    for i in range(len(point_grid)):
        for j in range(len(point_grid[i])):
            sum = 0
            n = 0
            for k in data:
                if lon_array[j] + step >= k.longitude >= lon_array[j] - step and lat_array[i] + step >= k.latitude >= lat_array[i] - step:
                    sum += k.data
                    n +=1
            point_grid[i][j] = int(math.log(sum / n, 1.5)) if n != 0 else sum
        print(i/len(point_grid))

    figure = plt.figure()
    ax = figure.add_subplot(111)
    contour = ax.contour(lon_array, lat_array, point_grid, levels=16, cmap=plt.cm.jet)
    geojson = geojsoncontour.contour_to_geojson(
        contour=contour,
        ndigits=3,
        unit='m'
    )
    return geojson


def get_heatmap(x1, x2, y1, y2, zoom):
    len_diag = ((x1 - x2)**2 + (y1 - y2)**2)**.5
    step = max((x1-x2)/1000, (y1-y2)/1000)
    data = get_data(x1, x2, y1, y2, step)
    lon_range, lat_range = np.mgrid[x2:x1:step, y2:y1:step] # 6 знаков после запятой
    Z = np.sinc(lon_range) * np.cos(lat_range)
    n_contours = 20
    levels = np.linspace(start=0, stop=100, num=n_contours)
    figure = plt.figure()
    ax = figure.add_subplot(111)
    contourf = ax.contourf(lon_range, lat_range, Z, levels=levels, cmap=plt.cm.jet)
    geojson = geojsoncontour.contourf_to_geojson(
        contourf=contourf,
        ndigits=3,
        unit='m'
    )
    return geojson


def my_custom_sql(self):
    with connection.cursor() as cursor:
        cursor.execute(self)
        row = cursor.fetchone()

    return row

def get_data(x1, x2, y1, y2, step):
    data = list(Measurement.objects.all())
    return [i for i in data if x1 + step >= i.longitude >= x2 - step and y1 + step >= i.latitude >= y2 - step]