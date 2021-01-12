import numpy as np


lon_range, lat_range = np.mgrid[0:1000, 0:1000] # 6 знаков после запятой
Z = np.sinc(lon_range) * np.cos(lat_range)
data = np.ndarray(shape=lon_range.shape)
for i in real_data:
    data[lon_range.index(i.longitude)][lat_range.index(i.latitude)] = data.data