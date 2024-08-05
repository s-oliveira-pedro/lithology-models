import os
import numpy as np

from numpy.random import rand

from landlab.grid import VoronoiDelaunayGrid


x, y = rand(25), rand(25)
vero_mg = VoronoiDelaunayGrid(x, y)

z_vero = vero_mg.add_zeros('topographic__elevation', at='node')
z_vero += np.random.rand(vero_mg.size)
#
# output_dir = '/Users/poliveira/Library/CloudStorage/OneDrive-CityUniversityofNewYork/PhD_LIFE/PhD_2nd_Chapter/diff_model_equi'
# os.makedirs(output_dir, exist_ok=True)