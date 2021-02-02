import numpy as np
import matplotlib.pyplot as plt 
import geojsoncontour
import pandas as pd
from django.db import connection
from scipy.interpolate.ndgriddata import griddata
from main.models import Measurement
from numba import njit, prange
from scipy.interpolate import SmoothBivariateSpline


@njit(fastmath=True, parallel=True)
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


def delete_nans(point_grid, lon_array, lat_array):
    point_grid = point_grid.ravel()
    lon_array = lon_array.ravel()
    lon_array = np.asarray(lon_array[point_grid!=np.isnan])
    lat_array = lat_array.ravel()
    lat_array = np.asarray(lat_array[point_grid!=np.isnan])
    point_grid = np.asarray(lat_array[point_grid!=np.isnan])
    return point_grid, lon_array, lat_array


def make_isolines(lon_array, lat_array, point_grid):
    figure = plt.figure()
    ax = figure.add_subplot(111)
    contour = ax.contour(lon_array, lat_array, point_grid, levels=range(0,17), cmap=plt.cm.jet)
    plt.show()
    geojson = geojsoncontour.contour_to_geojson(
        contour=contour,
        ndigits=3,
        unit='m',
    )
    return geojson


def prepare_table(x1, x2, y1, y2):
    step = max((x1-x2)/512, (y1-y2)/512)
    area = step / 2
    
    new_lon_array = np.asarray([round(i,6) for i in np.arange(x2,x1,step)]) #ширина 
    new_lat_array = np.asarray([round(i,6) for i in np.arange(y2,y1,step)]) #высота
    point_grid = np.zeros((len(new_lat_array), len(new_lon_array)))

    data = get_data(x1, x2, y1, y2, area)
    point_grid = fill_grid(point_grid, data, new_lon_array, new_lat_array, area)
    point_grid[point_grid == -1] = None
    
    return new_lon_array, new_lat_array, point_grid, 


def get_griddata(x1, x2, y1, y2):
    new_lon_array, new_lat_array, point_grid = prepare_table(x1, x2, y1, y2)
    
    lon_array, lat_array = np.meshgrid(new_lon_array, new_lat_array)
    point_grid, lon_array, lat_array = delete_nans(point_grid, lon_array, lat_array)
    new_point_grid = griddata((lon_array, lat_array), point_grid, (new_lon_array[None,:], new_lat_array[:,None]), method='linear')

    return make_isolines(new_lon_array, new_lat_array, new_point_grid)


def get_spline(x1, x2, y1, y2):
    new_lon_array, new_lat_array, point_grid = prepare_table(x1, x2, y1, y2)

    lon_array, lat_array = np.meshgrid(new_lon_array, new_lat_array)
    point_grid, lon_array, lat_array = delete_nans(point_grid, lon_array, lat_array)

    f = SmoothBivariateSpline(lon_array, lat_array, point_grid, kx=1, ky=1)
    new_point_grid = np.transpose(f(new_lon_array, new_lat_array))

    return make_isolines(new_lon_array, new_lat_array, new_point_grid)


def get_by_pandas(x1, x2, y1, y2):
    lon_array, lat_array, point_grid = prepare_table(x1, x2, y1, y2)

    df = pd.DataFrame(data=point_grid, index=lat_array, columns=lon_array, dtype=float)
    df = df.interpolate(method='pad', axis=0, limit_direction='forward')
    df = df.dropna(axis=0, how='all')
    df = df.dropna(axis=1, how='all')
    df = df.interpolate(method='pad', axis=0, limit_direction='forward')
    lat_array = df.index
    lon_array = df.columns
    point_grid = df.to_numpy()
    point_grid.tofile('data.txt',sep=' ')

    return make_isolines(lon_array, lat_array, point_grid)


def get_isolines(x1, x2, y1, y2, method):
    path = "{}.txt".format(method)
    with open(path, 'r') as f:
        file = f.read()
        return file if len(file) else fill_file(x1, x2, y1, y2, path)


def fill_file(x1, x2, y1, y2, path):
    if 'griddata' in path:
        file = get_griddata(x1, x2, y1, y2) 
    elif 'spline' in path:
        file = get_spline(x1, x2, y1, y2) 
    else:
        file = get_by_pandas(x1, x2, y1, y2)  
    with open(path, 'w') as f:
        f.write(file)
    return file


def get_heatmap(x1, x2, y1, y2):
    step = max((x1-x2)/((10*2**((21)/2))), (y1-y2)/((10*2**((21)/2))))
    area = step 
    data = get_data(x1, x2, y1, y2, area)
    lon_array = np.asarray([i for i in np.arange(x2,x1,step)]) #ширина 
    lat_array = np.asarray([i for i in np.arange(y2,y1,step)]) #высота
    point_grid = np.zeros((len(lat_array), len(lon_array)))
    print(len(lon_array)* len(lat_array))
    point_grid = fill_grid(point_grid, data, lon_array, lat_array, area)
    point_grid.tofile('data1.txt',sep=' ')

    df = pd.DataFrame(data=point_grid, index=lat_array, columns=lon_array, dtype=float)
    point_grid = df.interpolate(method='pad', axis=0, limit_area='outside')
    df = df.dropna(axis=0, how='all')
    lat_array = point_grid.index
    lon_array = point_grid.columns
    point_grid = point_grid.to_numpy()
    point_grid.tofile('data2.txt',sep=' ')

    figure = plt.figure()
    ax = figure.add_subplot(111)
    contourf = ax.contourf(lon_array, lat_array, point_grid, levels=range(0,16), cmap=plt.cm.jet)
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
    Measurements = list(Measurement.objects.filter(longitude__gte= x2 - step, longitude__lte= x1 + step, latitude__gte= y2 - step, latitude__lte= y1 + step))
    data = np.asarray([[i.data, float(i.longitude), float(i.latitude)]  for i in Measurements])
    return data