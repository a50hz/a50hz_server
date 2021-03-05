import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import geojsoncontour
import math
from django.db import connection
from scipy.interpolate.ndgriddata import griddata
from main.models import Extent, Measurement, Plot
from numba import jit, prange
from scipy.interpolate import Rbf


levels = range(0, 41)
resolution = 50
mul = 1
# заполнение сетки значениями точек
@jit(fastmath=True, parallel=True, nopython=True)
def fill_grid(grid, data, lon_array, lat_array, area):
    for i in prange(len(grid)):
        for j in prange(len(grid[i])):
            sum = 0.0
            n = 0.0
            for k in data:
                if lon_array[j] + area >= k[1] >= lon_array[j] - area and lat_array[i] + area >= k[2] >= lat_array[i] - area:
                    sum = sum + k[0]
                    n = n + 1
            if n!=0:
                if (sum // n) < 110:
                    grid[i][j] = math.ceil((sum / (2.5 * n)) - 4)
                else:
                    grid[i][j] = 40
            else:
                grid[i][j] = 16
    return grid


# получение точек по экстенту
def get_data(lat1, lat2, lng1, lng2, step):
    Measurements = list(Measurement.objects.filter(longitude__gte= lng1 - step, longitude__lte= lng2 + step, latitude__gte= lat1 - step, latitude__lte= lat2 + step))
    data = np.asarray([[int(i.data), float(i.longitude), float(i.latitude)]  for i in Measurements])
    return data

# первоначальное создание неообходимых для обработки массивов
def prepare_table(lat1, lat2, lng1, lng2):
    step = max((lat2-lat1)/resolution, (lng2-lng1)/resolution)
    area = step / 2
    
    lat_array = np.asarray([round(i,6) for i in np.arange(lat1,lat2,step)]) #ширина 
    lon_array = np.asarray([round(i,6) for i in np.arange(lng1,lng2,step)]) #высота
    point_grid = np.zeros((len(lat_array), len(lon_array)))
    data = get_data(lat1, lat2, lng1, lng2, area)
    point_grid = fill_grid(point_grid, data, lon_array, lat_array, area)
    
    return lon_array, lat_array, point_grid 

# построение изолиний из обработанных данных
def make_isolines(lon_array, lat_array, point_grid):
    figure = plt.figure()
    ax = figure.add_subplot(111)
    contour = ax.contour(lon_array, lat_array, point_grid, levels=levels, cmap=plt.cm.jet)
    geojson = geojsoncontour.contour_to_geojson(
        contour=contour,
        ndigits=3,
        unit='nT',
    )
    return geojson

# построение теплововой карты из обработанных данных
def make_heatmap(lon_array, lat_array, point_grid): 
    figure = plt.figure()
    ax = figure.add_subplot(111)
    contourf = ax.contourf(lon_array, lat_array, point_grid, levels=levels, cmap=plt.cm.jet)
    geojson = geojsoncontour.contourf_to_geojson(
        contourf=contourf,
        ndigits=3,
        unit='nT',
    )
    return geojson

# обработка с помощью griddata
def get_griddata(lon, lat, point_grid):
    point_grid = point_grid.reshape(len(lon), len(lat))
    lon, lat = np.meshgrid(lon, lat)

    new_lat, new_lon = np.meshgrid(np.linspace(lat[0], lat[-1], len(lat)*mul), np.linspace(lon[0], lon[-1], len(lon)*mul))
    xi=(new_lat, new_lon)
    points=np.array([lat.ravel(), lon.ravel()]).T
    values=point_grid.ravel()

    res = griddata(points, values, xi, method='linear')

    return new_lon, new_lat, res


# обработка rfb
def get_rbf(lon, lat, point_grid):
    point_grid = point_grid.reshape(len(lat), len(lon))
    new_lat = np.linspace(lat[0], lat[-1], len(lat)*mul)
    new_lon = np.linspace(lon[0], lon[-1], len(lon)*mul)
    lon, lat = np.meshgrid(lon, lat) # не трожь, ебанёт

    inter_func = Rbf(lat, lon, point_grid, function='linear', smooth=0)

    new_lat, new_lon = np.meshgrid(new_lat, new_lon) 
    res = inter_func(new_lat, new_lon)
    return new_lon, new_lat, res

# получение обработанных массивов
def get_processed_data(lon_array, lat_array, point_grid, method):
    if method == 'griddata':
        return get_griddata(lon_array, lat_array, point_grid)
    elif method == 'rbf':
        return get_rbf(lon_array, lat_array, point_grid)

# создание графика
def set_plot(data, kind):
    if kind == 'isolines':
        return make_isolines(*data)
    else:
        return make_heatmap(*data)


def update():
    for extent in Extent.objects.all():
        coordinates = [extent.lat1, extent.lat2, extent.lng1, extent.lng2]
        coordinates = map(float, coordinates)
        lon_array, lat_array, point_grid = prepare_table(*coordinates)
        for method in ['griddata', 'rbf']:
            data = get_processed_data(lon_array, lat_array, point_grid, method)
            for kind in ['isolines', 'heatmap']:
                plot = bytearray(set_plot(data, kind), 'utf-8')
                result = Plot.objects.create(value=plot, kind=kind, interpolation_type=method, Extent=extent)  
                print("Plot added!")
    

# для запросов через sql
def my_custom_sql(self):
    with connection.cursor() as cursor:
        cursor.execute(self)
        row = cursor.fetchone()

    return row


# удаление None значений
def delete_nans(point_grid, lon_array, lat_array):
    point_grid = point_grid.ravel()
    lon_array = lon_array.ravel()
    lat_array = lat_array.ravel()
    lon_array = np.asarray(lon_array[point_grid!=np.isnan])
    lat_array = np.asarray(lat_array[point_grid!=np.isnan])
    point_grid = np.asarray(point_grid[point_grid!=np.isnan])
    return point_grid, lon_array, lat_array