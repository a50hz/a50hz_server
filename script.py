import numpy as np
import matplotlib.pyplot as plt 
import geojsoncontour
import pandas as pd
from django.db import connection
from scipy.interpolate.ndgriddata import griddata
from main.models import Extent, Measurement, Plot
from numba import jit, prange
from scipy.interpolate import SmoothBivariateSpline

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
                grid[i][j] = np.log(sum / n)/np.log(1.5)
            else:
                grid[i][j] = -1
    return grid

# удаление None значений
def delete_nans(point_grid, lon_array, lat_array):
    point_grid = point_grid.ravel()
    lon_array = lon_array.ravel()
    lon_array = np.asarray(lon_array[point_grid!=np.isnan])
    lat_array = lat_array.ravel()
    lat_array = np.asarray(lat_array[point_grid!=np.isnan])
    point_grid = np.asarray(lat_array[point_grid!=np.isnan])
    return point_grid, lon_array, lat_array

# получение точек по экстенту
def get_data(lat1, lat2, lng1, lng2, step):
    Measurements = list(Measurement.objects.filter(longitude__gte= lng1 - step, longitude__lte= lng2 + step, latitude__gte= lat1 - step, latitude__lte= lat2 + step))
    data = np.asarray([[int(i.data), float(i.longitude), float(i.latitude)]  for i in Measurements])
    return data

# первоначальное создание неообходимых для обработки массивов
def prepare_table(lat1, lat2, lng1, lng2):
    step = max((lat2-lat1)/2048, (lng2-lng1)/2048)
    area = step / 2
    
    new_lat_array = np.asarray([round(i,6) for i in np.arange(lat1,lat2,step)]) #ширина 
    new_lon_array = np.asarray([round(i,6) for i in np.arange(lng1,lng2,step)]) #высота
    point_grid = np.zeros((len(new_lat_array), len(new_lon_array)))
    data = get_data(lat1, lat2, lng1, lng2, area)
    point_grid = fill_grid(point_grid, data, new_lon_array, new_lat_array, area)
    point_grid[point_grid == -1] = None
    
    return new_lon_array, new_lat_array, point_grid 

# построение изолиний из обработанных данных
def make_isolines(lon_array, lat_array, point_grid):
    figure = plt.figure()
    ax = figure.add_subplot(111)
    contour = ax.contour(lon_array, lat_array, point_grid, levels=range(0,17), cmap=plt.cm.jet)
    geojson = geojsoncontour.contour_to_geojson(
        contour=contour,
        ndigits=3,
        unit='m',
    )
    return geojson

# построение теплововой карты из обработанных данных
def make_heatmap(lon_array, lat_array, point_grid):
    figure = plt.figure()
    ax = figure.add_subplot(111)
    contourf = ax.contourf(lon_array, lat_array, point_grid, levels=range(0,17), cmap=plt.cm.jet)
    geojson = geojsoncontour.contourf_to_geojson(
        contourf=contourf,
        ndigits=3,
        unit='m',
    )
    return geojson

# обработка встроенная
def get_griddata(new_lon_array, new_lat_array, point_grid):

    lon_array, lat_array = np.meshgrid(new_lon_array, new_lat_array)
    point_grid, lon_array, lat_array = delete_nans(point_grid, lon_array, lat_array)
    new_point_grid = griddata((lon_array, lat_array), point_grid, (new_lon_array[None,:], new_lat_array[:,None]), method='linear')

    return new_lon_array, new_lat_array, new_point_grid

# обработка с помощью сплайна
def get_spline(new_lon_array, new_lat_array, point_grid):

    lon_array, lat_array = np.meshgrid(new_lon_array, new_lat_array)
    point_grid, lon_array, lat_array = delete_nans(point_grid, lon_array, lat_array)

    f = SmoothBivariateSpline(lon_array, lat_array, point_grid, kx=1, ky=1)
    new_point_grid = np.transpose(f(new_lon_array, new_lat_array))

    return new_lon_array, new_lat_array, new_point_grid

# обработка пандасом
def get_by_pandas(lon_array, lat_array, point_grid):
    df = pd.DataFrame(data=point_grid, index=lat_array, columns=lon_array, dtype=float)
    df = df.interpolate(method='pad', axis=1, limit_direction='forward')
    df = df.dropna(axis=0, how='all')
    df = df.dropna(axis=1, how='all')
    df = df.interpolate(method='pad', axis=0, limit_direction='forward')
    lat_array = df.index
    lon_array = df.columns
    point_grid = df.to_numpy()

    return lon_array, lat_array, point_grid

# получение обработанных массивов
def get_processed_data(lon_array, lat_array, point_grid, method):
    if method == 'griddata':
        return get_griddata(lon_array, lat_array, point_grid)
    elif method == 'spline':
        return get_spline(lon_array, lat_array, point_grid)
    else:
        return get_by_pandas(lon_array, lat_array, point_grid)

# создание графика
def set_plot(data, type):
    if type == 'isolines':
        return make_isolines(*data)
    else:
        return make_heatmap(*data)


def update():
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
    

# для запросов через sql
def my_custom_sql(self):
    with connection.cursor() as cursor:
        cursor.execute(self)
        row = cursor.fetchone()

    return row