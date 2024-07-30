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
basin_mg1 = RasterModelGrid((250,250),dx)
basin_mg2 = RasterModelGrid((250,250),dx)

folder_path = '/Users/poliveira/Library/CloudStorage/OneDrive-CityUniversityofNewYork/PhD_LIFE/PhD_2nd_Chapter/model_equi'
file_name = 'model_equi100000years.txt'
file_path = os.path.join(folder_path, file_name)

basin_mg1.at_node['topographic__elevation'] = np.loadtxt(file_path)
basin_mg2.at_node['topographic__elevation'] = np.loadtxt(file_path)

z1 = basin_mg1.at_node['topographic__elevation']
z2 = basin_mg2.at_node['topographic__elevation']

basin_mg1.set_closed_boundaries_at_grid_edges(True, True, False, True)
basin_mg2.set_closed_boundaries_at_grid_edges(True, True, False, True)

attrs = {'K_sp': {0: 5e-6, 1: 5e-7}}

z0s1 = 10 * np.arange(-1, 1)
z0s1[-1] = z0s1[-2] + 1000

z0s2 = 50 * np.arange(-1, 1)
z0s2[-1] = z0s2[-2] + 1000

print(z0s2)

ids = np.tile([0, 1], 1)
# z = ax + by + c
func_5d = lambda x, y: ((0.1 * x) + (0 * y))
func_26d = lambda x, y: ((0.5 * x) + (0 * y))

lith1 = LithoLayers(basin_mg1, z0s1, ids, function=func_5d, attrs=attrs)
lith2 = LithoLayers(basin_mg2, z0s2, ids, function=func_26d, attrs=attrs)


imshow_grid(basin_mg1, 'K_sp',cmap='viridis')
plt.show()
imshow_grid(basin_mg2, 'K_sp',cmap='viridis')
plt.show()

#
# U = 0.00004
# dt = 1000
# n_steps = 50001
#
# #%%
# ds1 = xr.Dataset(
#     data_vars={
#         'topographic__elevation': (
#             ('time', 'y', 'x'),  # tuple of dimensions
#             np.empty((n_steps, basin_mg1.shape[0], basin_mg1.shape[1])),  # n-d array of data
#             {
#                 'units': 'meters',  # dictionary with data attributes
#                 'long_name': 'Topographic Elevation'
#             }),
#         'rock_type__id':
#         (('time', 'y', 'x'), np.empty((n_steps, basin_mg1.shape[0], basin_mg1.shape[1])), {
#             'units': '-',
#             'long_name': 'Rock Type ID Code'
#         })
#     },
#     coords={
#         'x': (
#             ('x'),  # tuple of dimensions
#             basin_mg1.x_of_node.reshape(
#                 basin_mg1.shape)[0, :],  # 1-d array of coordinate data
#             {
#                 'units': 'meters'
#             }),  # dictionary with data attributes
#         'y': (('y'), basin_mg2.y_of_node.reshape(basin_mg1.shape)[:, 1], {
#             'units': 'meters'
#         }),
#         'time': (('time'), dt * np.arange(n_steps) / 1e6, {
#             'units': 'millions of years since model start',
#             'standard_name': 'time'
#         })
#     })
#
# ds2 = xr.Dataset(
#     data_vars={
#         'topographic__elevation': (
#             ('time', 'y', 'x'),  # tuple of dimensions
#             np.empty((n_steps, basin_mg2.shape[0], basin_mg2.shape[1])),  # n-d array of data
#             {
#                 'units': 'meters',  # dictionary with data attributes
#                 'long_name': 'Topographic Elevation'
#             }),
#         'rock_type__id':
#             (('time', 'y', 'x'), np.empty((n_steps, basin_mg2.shape[0], basin_mg2.shape[1])), {
#                 'units': '-',
#                 'long_name': 'Rock Type ID Code'
#             })
#     },
#     coords={
#         'x': (
#             ('x'),  # tuple of dimensions
#             basin_mg2.x_of_node.reshape(
#                 basin_mg2.shape)[0, :],  # 1-d array of coordinate data
#             {
#                 'units': 'meters'
#             }),  # dictionary with data attributes
#         'y': (('y'), basin_mg2.y_of_node.reshape(basin_mg2.shape)[:, 1], {
#             'units': 'meters'
#         }),
#         'time': (('time'), dt * np.arange(n_steps) / 1e6, {
#             'units': 'millions of years since model start',
#             'standard_name': 'time'
#         })
#     })
#
# fa1 = FlowAccumulator(basin_mg1, flow_director="D8", depression_finder="DepressionFinderAndRouter")
# sp1 = FastscapeEroder(basin_mg1, K_sp='K_sp')
#
# fa2 = FlowAccumulator(basin_mg2, flow_director="D8", depression_finder="DepressionFinderAndRouter")
# sp2 = FastscapeEroder(basin_mg2, K_sp='K_sp')
#
# out_fields = ['topographic__elevation', 'rock_type__id']
#
# for i in range(n_steps):
#
#     fa1.run_one_step()
#     sp1.run_one_step(dt=dt)
#     fa2.run_one_step()
#     sp2.run_one_step(dt=dt)
#
#     dz_ad1 = np.zeros(basin_mg1.size('node'))
#     dz_ad1[basin_mg1.core_nodes] = U * dt
#     z1 += dz_ad1
#     lith1.dz_advection = dz_ad1
#     lith1.run_one_step()
#
#     dz_ad2 = np.zeros(basin_mg2.size('node'))
#     dz_ad2[basin_mg2.core_nodes] = U * dt
#     z2 += dz_ad2
#     lith2.dz_advection = dz_ad2
#     lith2.run_one_step()
#
#     for of in out_fields:
#         ds1[of][i, :, :] = basin_mg1['node'][of].reshape(basin_mg1.shape)
#     for of in out_fields:
#         ds2[of][i, :, :] = basin_mg2['node'][of].reshape(basin_mg2.shape)
#
#     print(i)
#
#     if i%200==0:
#         save_directory = "/Users/poliveira/Library/CloudStorage/OneDrive-CityUniversityofNewYork/PhD_LIFE/PhD_2nd_Chapter/model_diff_angle_1"
#
#         fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(4, 4))
#
#         plt.sca(ax1)
#         imshow_grid(basin_mg1, 'topographic__elevation',cmap='viridis')
#         ax1.set_title('Elevation')
#
#         plt.sca(ax2)
#         imshow_grid(basin_mg1, 'K_sp',cmap='viridis')
#         ax2.set_title('K_sp')
#
#         plt.sca(ax3)
#         imshow_grid(basin_mg2, 'topographic__elevation', cmap='viridis')
#         ax1.set_title('Elevation')
#
#         plt.sca(ax4)
#         imshow_grid(basin_mg2, 'K_sp', cmap='viridis')
#         ax2.set_title('K_sp')
#
#         plt.tight_layout()
#
#         plot_filename = os.path.join(save_directory, "model_diff_angle_1_" + str((i + 1) * dt) + "_yrs.png")
#         plt.savefig(plot_filename)
#
#         data_filename1 = os.path.join(save_directory, "topo1_model_diff_angle_1_" + str((i + 1) * dt) + " yrs.txt")
#         data_filename2 = os.path.join(save_directory, "ksp1_model_diff_angle_1_" + str((i + 1) * dt) + " yrs.txt")
#         data_filename3 = os.path.join(save_directory, "topo2_model_diff_angle_1_" + str((i + 1) * dt) + " yrs.txt")
#         data_filename4 = os.path.join(save_directory, "ksp2_model_diff_angle_1_" + str((i + 1) * dt) + " yrs.txt")
#
#         np.savetxt(data_filename1, basin_mg1.at_node['topographic__elevation'])
#         np.savetxt(data_filename2, basin_mg1.at_node['K_sp'])
#         np.savetxt(data_filename3, basin_mg2.at_node['topographic__elevation'])
#         np.savetxt(data_filename4, basin_mg2.at_node['K_sp'])
#
#         z_1c = z1.copy()
#         z_2c = z2.copy()
#
#         del lith1
#         del lith2
#         del z1
#         del z2
#         del basin_mg1
#         del basin_mg2
#         del fa1
#         del sp1
#         del fa2
#         del sp2
#
#         basin_mg1 = RasterModelGrid((150, 150), dx)
#         basin_mg2 = RasterModelGrid((150, 150), dx)
#
#         basin_mg1.set_closed_boundaries_at_grid_edges(True, True, False, True)
#         basin_mg2.set_closed_boundaries_at_grid_edges(True, True, False, True)
#
#         basin_mg1.at_node['topographic__elevation'] = z_1c
#         basin_mg2.at_node['topographic__elevation'] = z_2c
#
#         z1 = basin_mg1.at_node['topographic__elevation']
#         z2 = basin_mg2.at_node['topographic__elevation']
#
#         lith1 = LithoLayers(basin_mg1, z0s1, ids, function=func_5d, attrs=attrs)
#         lith2 = LithoLayers(basin_mg2, z0s2, ids, function=func_26d, attrs=attrs)
#
#         fa1 = FlowAccumulator(basin_mg1, flow_director="D8", depression_finder="DepressionFinderAndRouter")
#         sp1 = FastscapeEroder(basin_mg1, K_sp='K_sp')
#
#         fa2 = FlowAccumulator(basin_mg2, flow_director="D8", depression_finder="DepressionFinderAndRouter")
#         sp2 = FastscapeEroder(basin_mg2, K_sp='K_sp')
#






