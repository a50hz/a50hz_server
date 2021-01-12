import numpy as np
import matplotlib.pyplot as plt
import geojsoncontour
from main.models import Measurement


def get_isolines(x1, x2, y1, y2):
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


def g1et_isolines(x1, x2, y1, y2):
    data = get_data(x1, x2, y1, y2)
    step = min((x1-x2)/1000, (y1-y2)/1000)
    lon_array = [i for i in np.arange(x2,x1,step)]
    lat_array = [i for i in np.arange(y2,y1,step)]

    point_grid = np.zeros(
        (len(lon_array), len(lat_array))
    )

    for id, value in enumerate(point_grid):
        for j in value:
            data = Measurement.objects.raw("SELECT * FROM public.main_measurement WHERE ({} < longitude) and (longitude < {}) and ({} < latitude) and (latitude < {})".format((lon_array[id]-step), (lon_array[id]+step), (lat_array[id]-step), (lat_array[id]+step)))

    figure = plt.figure()
    ax = figure.add_subplot(111)
    contour = ax.contour(lon_array, lat_array, Z, level=16, cmap=plt.cm.jet)
    geojson = geojsoncontour.contour_to_geojson(
        contour=contour,
        ndigits=3,
        unit='m'
    )
    return geojson


def get_heatmap(x1, x2, y1, y2):
    data = get_data(x1, x2, y1, y2)
    len_diag = ((x1 - x2)**2 + (y1 - y2)**2)**.5
    step_x = (x1-x2)/1000
    step_y = (y1-y2)/1000
    lon_range, lat_range = np.mgrid[x2:x1:step_x, y2:y1:step_y] # 6 знаков после запятой
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


def get_data(x1, x2, y1, y2):
    data = list(Measurement.objects.all())
    return [i for i in data if x1 >= i.longitude >= x2 and y1 >= i.latitude >= y2]