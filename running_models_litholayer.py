import os
import numpy as np
import matplotlib.pyplot as plt
from landlab import RasterModelGrid
from landlab.components import FlowAccumulator, FastscapeEroder, LinearDiffuser, Lithology, LithoLayers
from landlab.plot import imshow_grid
from litholayers_module import Litho_models

dx=50
basin_mg = RasterModelGrid((250,250),dx)

folder_path = '/Users/poliveira/Library/CloudStorage/OneDrive-CityUniversityofNewYork/PhD_LIFE/PhD_2nd_Chapter/model_equi'
file_name = 'model_equi100000years.txt'

file_path = os.path.join(folder_path, file_name)

basin_mg.at_node['topographic__elevation'] = np.loadtxt(file_path)
basin_mg.set_closed_boundaries_at_grid_edges(True, True, False, True)

z = basin_mg.at_node['topographic__elevation']

thickness = 200
attrs = {'K_sp': {0: 0.0000005, 1: 0.00000001}}

z0s = thickness * np.arange(-5, 5)

ids = np.tile([0, 1], 5)

# z = ax + by + c*0
a=1
b=1

model = Litho_models(a,b,thickness)
an = model.angle_between_plane_and_horizontal()
se = model.calculate_surface_exposure()
sp = model.strike_plane()

func_5d = lambda x, y: ((a * x) + (b * y))

lith = LithoLayers(basin_mg, z0s, ids, function=func_5d, attrs=attrs)

imshow_grid(basin_mg, 'rock_type__id', cmap='viridis',plot_name=f"Dip:{an: .2f} Outcrop:{se: .2f} Strike:{sp: .2f}")
plt.show()

# U = 0.00001
# dt = 1000
# n_steps = 100001
#
# ds = xr.Dataset(
#     data_vars={
#         'topographic__elevation': (
#             ('time', 'y', 'x'),  # tuple of dimensions
#             np.empty((n_steps, basin_mg.shape[0], basin_mg.shape[1])),  # n-d array of data
#             {
#                 'units': 'meters',  # dictionary with data attributes
#                 'long_name': 'Topographic Elevation'
#             }),
#         'rock_type__id':
#         (('time', 'y', 'x'), np.empty((n_steps, basin_mg.shape[0], basin_mg.shape[1])), {
#             'units': '-',
#             'long_name': 'Rock Type ID Code'
#         })
#     },
#     coords={
#         'x': (
#             ('x'),  # tuple of dimensions
#             basin_mg.x_of_node.reshape(
#                 basin_mg.shape)[0, :],  # 1-d array of coordinate data
#             {
#                 'units': 'meters'
#             }),  # dictionary with data attributes
#         'y': (('y'), basin_mg.y_of_node.reshape(basin_mg.shape)[:, 1], {
#             'units': 'meters'
#         }),
#         'time': (('time'), dt * np.arange(n_steps) / 1e6, {
#             'units': 'millions of years since model start',
#             'standard_name': 'time'
#         })
#     })
#
#
# fa = FlowAccumulator(basin_mg, flow_director="D8", depression_finder="DepressionFinderAndRouter")
# sp = FastscapeEroder(basin_mg, K_sp='K_sp')
#
# print(ds)
# ds.topographic__elevation
#
# out_fields = ['topographic__elevation', 'rock_type__id']
#
# for i in range(n_steps):
#     fa.run_one_step()
#     sp.run_one_step(dt=dt)
#     dz_ad = np.zeros(basin_mg.size('node'))
#     dz_ad[basin_mg.core_nodes] = U * dt
#     z += dz_ad
#     lith.dz_advection = dz_ad
#     lith.run_one_step()
#     print(i)
#
#     for of in out_fields:
#         ds[of][i, :, :] = basin_mg['node'][of].reshape(basin_mg.shape)
#
#     if i % 1000 == 0:
#         save_directory = "/Users/poliveira/Library/CloudStorage/OneDrive-CityUniversityofNewYork/PhD_LIFE/PhD_2nd_Chapter/model_lito_2"
#
#         fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
#
#         # Set the current axis to the first subplot and plot the first image
#         plt.sca(ax1)
#         imshow_grid(basin_mg, 'topographic__elevation')
#         ax1.set_title('Elevation')
#
#         # Set the current axis to the second subplot and plot the second image
#         plt.sca(ax2)
#         imshow_grid(basin_mg, 'K_sp')
#         ax2.set_title('K_sp')
#
#         # Adjust layout
#         plt.tight_layout()
#
#         # Save the figure
#         plot_filename = os.path.join(save_directory, "model_lito_2_" + str((i + 1) * dt) + "_yrs.png")
#
#         # Save the plot
#         plt.savefig(plot_filename)
#
#         # Show the plot
#         #plt.show()
#
#         # Close the plot
#         plt.close()
#
#         # Define the full path to the data file
#         data_filename = os.path.join(save_directory, "model_lito_2_" + str((i + 1) * dt) + " yrs.txt")
#
#         # Save the data
#         np.savetxt(data_filename, basin_mg.at_node['topographic__elevation'])



