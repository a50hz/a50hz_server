import numpy as np
import matplotlib.pyplot as plt
import geojsoncontour
from django.db import connection
from main.models import Measurement


def pget_isolines(x1, x2, y1, y2):
    data = get_data(x1, x2, y1, y2)
    step = min((x1-x2)/1000, (y1-y2)/1000)
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


def get_isolines(x1, x2, y1, y2):
    #data =  my_custom_sql("SELECT * FROM public.main_measurement WHERE ({} < longitude) and (longitude < {}) and ({} < latitude) and (latitude < {})".format((lon_array[i]-step), (lon_array[i]+step), (lat_array[j]-step), (lat_array[j]+step)))
    step = max((x1-x2)/1000, (y1-y2)/1000)
    data = get_data(x1, x2, y1, y2)
    lon_array = [i for i in np.arange(x2,x1,step)]
    lat_array = [i for i in np.arange(y2,y1,step)]

    point_grid = np.zeros(
        (len(lon_array), len(lat_array))
    )

    for i in range(len(lon_array)):
        for j in range(len(lat_array)):
            
            if data != None:
                point_grid[i][j] = data
        print(i)

    print(point_grid == np.zeros(
        (len(lon_array), len(lat_array))
    ))

    figure = plt.figure()
    ax = figure.add_subplot(111)
    contour = ax.contour(lon_array, lat_array, point_grid, level=16, cmap=plt.cm.jet)
    geojson = geojsoncontour.contour_to_geojson(
        contour=contour,
        ndigits=3,
        unit='m'
    )
    return geojson


def get_heatmap(x1, x2, y1, y2):
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
    return  my_custom_sql("SELECT id, data, longitude, latitude FROM public.main_measurement WHERE ({} < longitude) and (longitude < {}) and ({} < latitude) and (latitude < {})".format((x1-step), (x2+step), (y1-step), (y2+step)))