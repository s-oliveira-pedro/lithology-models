import os
import numpy as np
import matplotlib.pyplot as plt
from landlab import HexModelGrid
from landlab.components import FlowAccumulator, FastscapeEroder,LithoLayers,Lithology
from landlab.plot import imshow_grid
import xarray as xr


output_dir = '/Users/poliveira/Library/CloudStorage/OneDrive-CityUniversityofNewYork/PhD_LIFE/PhD_2nd_Chapter/diff_model_equi'
os.makedirs(output_dir, exist_ok=True)

dx= 25
hex_mg = HexModelGrid((100,50), dx)
z_hex = hex_mg.add_zeros('topographic__elevation', at='node')
z_hex += np.random.rand(z_hex.size)

hex_mg.set_watershed_boundary_condition_outlet_id(49, z_hex)

attrs = {'K_sp': {0: 0.0000005, 1: 0.00000001}}

z0s = 20 * np.arange(-3, 3)
z0s[-1] = z0s[-2] + 1000

ids = np.tile([0, 1], 3)

# z = ax + by + c
func_45d = lambda x, y: ((1 * x) + (0 * y))

lith = LithoLayers(hex_mg, z0s, ids, function=func_45d, attrs=attrs)


Uh = np.ones(hex_mg.number_of_nodes)
uplift_rate = 0.00005
Uh = Uh*uplift_rate

K_sp = 5E-6
dt = 1000
n_steps = 100001
uplift_per_step_h = dt * Uh

fa_h = FlowAccumulator(hex_mg, flow_director='Steepest',
                     depression_finder='DepressionFinderAndRouter')
sp_h = FastscapeEroder(hex_mg, K_sp=K_sp)

for i in range(n_steps):

    fa_h.run_one_step()
    sp_h.run_one_step(dt=dt)
    dz_ad = np.zeros(hex_mg.size('node'))
    dz_ad[hex_mg.core_nodes] = Uh * dt
    z_hex += dz_ad
    lith.dz_advection = dz_ad
    lith.run_one_step()

    for of in out_fields:
        ds[of][i, :, :] = hex_mg['node'][of].reshape(hex_mg.shape)

    print(i)

    if i % 1000 == 0:

        imshow_grid(hex_mg, 'topographic__elevation',cmap="terrain")
