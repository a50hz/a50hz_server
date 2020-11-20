import numpy as np
import matplotlib.pyplot as plt
import geojsoncontour
# import random


def prepare_file():
    lon_range, lat_range = np.mgrid[55.889:56.2:0.05, 54.675:54.95:0.01]
    Z = np.sinc(lon_range) * np.cos(lat_range)
    figure = plt.figure()
    ax = figure.add_subplot(111)
    contour = ax.contour(lon_range, lat_range, Z, cmap=plt.cm.RdYlGn)
    geojson = geojsoncontour.contour_to_geojson(
        contour=contour,
        ndigits=3,
        unit='m'
    )
    return geojson
    #f = open("C:/dev/geodjango/main/templates/main/data.json", "w+")
    #f.write(geojson)


def set_data():
    # Create contour data lon_range, lat_range, Z
    lon_range, lat_range = np.mgrid[55.889:56.2:0.0000005, 54.675:54.95:0.01]
    print(len(lon_range), len(lat_range))
    Z = np.sinc(lon_range) * np.cos(lat_range)
    # for i in range(len(lon_range)):
    #    for j in range(len(lat_range)):
    #       Z[i][j]=random.randint(0,15)
    # levels = [i for i in range(16)]
    # Create a contour plot plot from grid (lat, lon) data
    figure = plt.figure()
    ax = figure.add_subplot(111)
    contour = ax.contour(lon_range, lat_range, Z, cmap=plt.cm.RdYlGn)
    # Convert matplotlib contour to geojson plt.cm.jet
    geojson = geojsoncontour.contour_to_geojson(
        contour=contour,
        ndigits=3,
        unit='m'
    )
    f = open("C:/Data/MyVKR/vkr/main/templates/main/data.json", "w+")
    f.write(geojson)
