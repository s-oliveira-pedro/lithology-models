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
basin_mg1 = RasterModelGrid((150,150),dx)
basin_mg2 = RasterModelGrid((150,150),dx)
basin_mg3 = RasterModelGrid((150,150),dx)

folder_path = '/Users/poliveira/Library/CloudStorage/OneDrive-CityUniversityofNewYork/PhD_LIFE/PhD_2nd_Chapter/model_equi'
file_name = 'model_equi100000years.txt'
file_path = os.path.join(folder_path, file_name)

basin_mg1.at_node['topographic__elevation'] = np.loadtxt(file_path)
basin_mg2.at_node['topographic__elevation'] = np.loadtxt(file_path)
basin_mg3.at_node['topographic__elevation'] = np.loadtxt(file_path)

z1 = basin_mg1.at_node['topographic__elevation']
z2 = basin_mg2.at_node['topographic__elevation']
z3 = basin_mg3.at_node['topographic__elevation']

basin_mg1.set_closed_boundaries_at_grid_edges(True, True, False, True)
basin_mg2.set_closed_boundaries_at_grid_edges(True, True, False, True)
basin_mg3.set_closed_boundaries_at_grid_edges(True, True, False, True)

attrs = {'K_sp': {0: 0.0000005, 1: 0.00000001}}

z0s1 = 25 * np.arange(-1, 1)
z0s1[-1] = z0s1[-2] + 1000

z0s2 = 50 * np.arange(-1, 1)
z0s2[-1] = z0s2[-2] + 1000

z0s3 = 75 * np.arange(-1, 1)
z0s3[-1] = z0s3[-2] + 1000

ids = np.tile([0, 1], 1)
# z = ax + by + c
func_5d = lambda x, y: ((0.3 * x) + (0 * y))

lith1 = LithoLayers(basin_mg1, z0s1, ids, function=func_5d, attrs=attrs)
lith2 = LithoLayers(basin_mg2, z0s2, ids, function=func_5d, attrs=attrs)
lith3 = LithoLayers(basin_mg3, z0s3, ids, function=func_5d, attrs=attrs)

U = 0.00001
dt = 1000
n_steps = 50001

#%%
ds1 = xr.Dataset(
    data_vars={
        'topographic__elevation': (
            ('time', 'y', 'x'),  # tuple of dimensions
            np.empty((n_steps, basin_mg1.shape[0], basin_mg1.shape[1])),  # n-d array of data
            {
                'units': 'meters',  # dictionary with data attributes
                'long_name': 'Topographic Elevation'
            }),
        'rock_type__id':
        (('time', 'y', 'x'), np.empty((n_steps, basin_mg1.shape[0], basin_mg1.shape[1])), {
            'units': '-',
            'long_name': 'Rock Type ID Code'
        })
    },
    coords={
        'x': (
            ('x'),  # tuple of dimensions
            basin_mg1.x_of_node.reshape(
                basin_mg1.shape)[0, :],  # 1-d array of coordinate data
            {
                'units': 'meters'
            }),  # dictionary with data attributes
        'y': (('y'), basin_mg2.y_of_node.reshape(basin_mg1.shape)[:, 1], {
            'units': 'meters'
        }),
        'time': (('time'), dt * np.arange(n_steps) / 1e6, {
            'units': 'millions of years since model start',
            'standard_name': 'time'
        })
    })

ds2 = xr.Dataset(
    data_vars={
        'topographic__elevation': (
            ('time', 'y', 'x'),  # tuple of dimensions
            np.empty((n_steps, basin_mg2.shape[0], basin_mg2.shape[1])),  # n-d array of data
            {
                'units': 'meters',  # dictionary with data attributes
                'long_name': 'Topographic Elevation'
            }),
        'rock_type__id':
            (('time', 'y', 'x'), np.empty((n_steps, basin_mg2.shape[0], basin_mg2.shape[1])), {
                'units': '-',
                'long_name': 'Rock Type ID Code'
            })
    },
    coords={
        'x': (
            ('x'),  # tuple of dimensions
            basin_mg2.x_of_node.reshape(
                basin_mg2.shape)[0, :],  # 1-d array of coordinate data
            {
                'units': 'meters'
            }),  # dictionary with data attributes
        'y': (('y'), basin_mg2.y_of_node.reshape(basin_mg2.shape)[:, 1], {
            'units': 'meters'
        }),
        'time': (('time'), dt * np.arange(n_steps) / 1e6, {
            'units': 'millions of years since model start',
            'standard_name': 'time'
        })
    })


ds3 = xr.Dataset(
    data_vars={
        'topographic__elevation': (
            ('time', 'y', 'x'),  # tuple of dimensions
            np.empty((n_steps, basin_mg3.shape[0], basin_mg3.shape[1])),  # n-d array of data
            {
                'units': 'meters',  # dictionary with data attributes
                'long_name': 'Topographic Elevation'
            }),
        'rock_type__id':
            (('time', 'y', 'x'), np.empty((n_steps, basin_mg3.shape[0], basin_mg3.shape[1])), {
                'units': '-',
                'long_name': 'Rock Type ID Code'
            })
    },
    coords={
        'x': (
            ('x'),  # tuple of dimensions
            basin_mg3.x_of_node.reshape(
                basin_mg3.shape)[0, :],  # 1-d array of coordinate data
            {
                'units': 'meters'
            }),  # dictionary with data attributes
        'y': (('y'), basin_mg3.y_of_node.reshape(basin_mg3.shape)[:, 1], {
            'units': 'meters'
        }),
        'time': (('time'), dt * np.arange(n_steps) / 1e6, {
            'units': 'millions of years since model start',
            'standard_name': 'time'
        })
    })

fa1 = FlowAccumulator(basin_mg1, flow_director="D8", depression_finder="DepressionFinderAndRouter")
sp1 = FastscapeEroder(basin_mg1, K_sp='K_sp')

fa2 = FlowAccumulator(basin_mg2, flow_director="D8", depression_finder="DepressionFinderAndRouter")
sp2 = FastscapeEroder(basin_mg2, K_sp='K_sp')

fa3 = FlowAccumulator(basin_mg3, flow_director="D8", depression_finder="DepressionFinderAndRouter")
sp3 = FastscapeEroder(basin_mg3, K_sp='K_sp')

out_fields = ['topographic__elevation', 'rock_type__id']

for i in range(n_steps):

    fa1.run_one_step()
    sp1.run_one_step(dt=dt)
    fa2.run_one_step()
    sp2.run_one_step(dt=dt)
    fa3.run_one_step()
    sp3.run_one_step(dt=dt)

    dz_ad1 = np.zeros(basin_mg1.size('node'))
    dz_ad1[basin_mg1.core_nodes] = U * dt
    z1 += dz_ad1
    lith1.dz_advection = dz_ad1
    lith1.run_one_step()

    dz_ad2 = np.zeros(basin_mg2.size('node'))
    dz_ad2[basin_mg2.core_nodes] = U * dt
    z2 += dz_ad2
    lith2.dz_advection = dz_ad2
    lith2.run_one_step()

    dz_ad3 = np.zeros(basin_mg3.size('node'))
    dz_ad3[basin_mg3.core_nodes] = U * dt
    z3 += dz_ad3
    lith3.dz_advection = dz_ad3
    lith3.run_one_step()

    for of in out_fields:
        ds1[of][i, :, :] = basin_mg1['node'][of].reshape(basin_mg1.shape)
    for of in out_fields:
        ds2[of][i, :, :] = basin_mg2['node'][of].reshape(basin_mg2.shape)
    for of in out_fields:
        ds3[of][i, :, :] = basin_mg3['node'][of].reshape(basin_mg3.shape)

    print(i)
    if i%5000==0:
        save_directory = "/Users/poliveira/Library/CloudStorage/OneDrive-CityUniversityofNewYork/PhD_LIFE/PhD_2nd_Chapter/model_low_angle_2"

        fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(6, 6))

        plt.sca(ax1)
        imshow_grid(basin_mg1, 'topographic__elevation',cmap='viridis')
        ax1.set_title('Elevation')

        plt.sca(ax2)
        imshow_grid(basin_mg1, 'K_sp',cmap='viridis')
        ax2.set_title('K_sp')

        plt.sca(ax3)
        imshow_grid(basin_mg2, 'topographic__elevation', cmap='viridis')
        ax1.set_title('Elevation')

        plt.sca(ax4)
        imshow_grid(basin_mg2, 'K_sp', cmap='viridis')
        ax2.set_title('K_sp')

        plt.sca(ax5)
        imshow_grid(basin_mg3, 'topographic__elevation', cmap='viridis')
        ax1.set_title('Elevation')

        plt.sca(ax6)
        imshow_grid(basin_mg3, 'K_sp', cmap='viridis')
        ax2.set_title('K_sp')

        plt.tight_layout()

        plot_filename = os.path.join(save_directory, "model_low_angle_2_" + str((i + 1) * dt) + "_yrs.png")
        plt.savefig(plot_filename)

        data_filename1 = os.path.join(save_directory, "topo1_model_low_angle_2_" + str((i + 1) * dt) + " yrs.txt")
        data_filename2 = os.path.join(save_directory, "ksp1_model_low_angle_2_" + str((i + 1) * dt) + " yrs.txt")
        data_filename3 = os.path.join(save_directory, "topo2_model_low_angle_2_" + str((i + 1) * dt) + " yrs.txt")
        data_filename4 = os.path.join(save_directory, "ksp2_model_low_angle_2_" + str((i + 1) * dt) + " yrs.txt")
        data_filename5 = os.path.join(save_directory, "topo3_model_low_angle_2_" + str((i + 1) * dt) + " yrs.txt")
        data_filename6 = os.path.join(save_directory, "ksp3_model_low_angle_2_" + str((i + 1) * dt) + " yrs.txt")

        np.savetxt(data_filename1, basin_mg1.at_node['topographic__elevation'])
        np.savetxt(data_filename2, basin_mg1.at_node['K_sp'])
        np.savetxt(data_filename3, basin_mg2.at_node['topographic__elevation'])
        np.savetxt(data_filename4, basin_mg2.at_node['K_sp'])
        np.savetxt(data_filename5, basin_mg3.at_node['topographic__elevation'])
        np.savetxt(data_filename6, basin_mg3.at_node['K_sp'])


