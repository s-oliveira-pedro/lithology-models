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
basin_mg = RasterModelGrid((150,150),dx)

folder_path = '/Users/poliveira/Library/CloudStorage/OneDrive-CityUniversityofNewYork/PhD_LIFE/PhD_2nd_Chapter/model_equi'
file_name = 'model_equi100000years.txt'

file_path = os.path.join(folder_path, file_name)

basin_mg.at_node['topographic__elevation'] = np.loadtxt(file_path)

z = basin_mg.at_node['topographic__elevation']

basin_mg.set_closed_boundaries_at_grid_edges(True, True, False, True)

attrs = {'K_sp': {0: 0.0000005, 1: 0.00000001}}

z0s = 100 * np.arange(-1, 1)
z0s[-1] = z0s[-2] + 1000

ids = np.tile([0, 1], 1)

# z = ax + by + c
func_5d = lambda x, y: ((0.1 * x) + (0 * y))

lith = LithoLayers(basin_mg, z0s, ids, function=func_5d, attrs=attrs)

imshow_grid(basin_mg, 'rock_type__id', cmap='viridis')
plt.show()

ds = lith.rock_cube_to_xarray(np.arange(300))
hvds_rock = hv.Dataset(ds.rock_type__id)

hvds_rock.to(hv.Image, ['x', 'z'])
