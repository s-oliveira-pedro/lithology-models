import warnings
warnings.filterwarnings('ignore')

import os
import numpy as np
import xarray as xr
import dask

import matplotlib
import matplotlib.pyplot as plt

import holoviews as hv
hv.extension('matplotlib')

from landlab import RasterModelGrid
from landlab.components import FlowAccumulator, FastscapeEroder, LinearDiffuser, Lithology, LithoLayers
from landlab.plot import imshow_grid

dx= 100
basin_mg = RasterModelGrid((250,250),dx)

folder_path = '/Users/poliveira/Library/CloudStorage/OneDrive-CityUniversityofNewYork/PhD_LIFE/PhD_2nd_Chapter/model_equi'
file_name = 'model_equi100000years.txt'

file_path = os.path.join(folder_path, file_name)

basin_mg.at_node['topographic__elevation'] = np.loadtxt(file_path)

z = basin_mg.at_node['topographic__elevation']

basin_mg.set_closed_boundaries_at_grid_edges(True, True, False, True)

attrs = {'K_sp': {0: 0.0000005, 1: 0.00000001}}

z0s = 500 * np.arange(-5, 5)
z0s[-1] = z0s[-2] + 1000

# z0s = [-10000, -5000, -4000, -3000, -2000, -1000,0,  1000,  2000,  3000,  4000]
# ids = [1,0, 1, 0, 0, 0, 0, 0, 0, 0, 0]

ids = np.tile([0, 1], 5)

# z = ax + by + c
func_5d = lambda x, y: ((0.7 * x) + (0 * y))

lith = LithoLayers(basin_mg, z0s, ids, function=func_5d, attrs=attrs)

print(z0s)
print(ids)

imshow_grid(basin_mg, 'rock_type__id', cmap='viridis')
plt.show()