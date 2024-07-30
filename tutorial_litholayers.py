#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 17:48:33 2024

@author: poliveira
"""

#import warnings
#warnings.filterwarnings('ignore')

import os
import numpy as np
import xarray as xr
import dask
import matplotlib.pyplot as plt

import holoviews as hv

from landlab import RasterModelGrid
from landlab.components import FlowAccumulator, FastscapeEroder, LinearDiffuser, Lithology, LithoLayers
from landlab.plot import imshow_grid

mg = RasterModelGrid((10, 15))
z = mg.add_zeros('topographic__elevation', at='node')

layer_elevations = 5. * np.arange(-10, 10)

# we create a bottom layer that is very thick.
layer_elevations[-1] = layer_elevations[-2] + 100

layer_ids = np.tile([0, 1, 2, 3], 5)

attrs = {'K_sp': {0: 0.0003, 1: 0.0001, 2: 0.0002, 3: 0.0004}}

func = lambda x, y: x + (2. * y)

lith = LithoLayers(mg, layer_elevations, layer_ids, function=func, attrs=attrs)

imshow_grid(mg, 'rock_type__id', cmap='viridis')

z -= 1.
dz_ad = 0.
lith.dz_advection=dz_ad
lith.run_one_step()

imshow_grid(mg, 'rock_type__id', cmap='viridis')