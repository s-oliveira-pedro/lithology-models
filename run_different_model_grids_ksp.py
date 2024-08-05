import os
import numpy as np
import matplotlib.pyplot as plt
from landlab import RasterModelGrid, HexModelGrid
from landlab.components import FlowAccumulator, FastscapeEroder
from landlab.plot import imshow_grid

output_dir = '/Users/poliveira/Library/CloudStorage/OneDrive-CityUniversityofNewYork/PhD_LIFE/PhD_2nd_Chapter/diff_model_gris_ksp'
os.makedirs(output_dir, exist_ok=True)

dx= 25

raster_mg = RasterModelGrid((100,100),dx)
hex_mg = HexModelGrid((100,50), dx)

z_raster = raster_mg.add_zeros('topographic__elevation', at='node')
z_raster += np.random.rand(z_raster.size)
z_hex = hex_mg.add_zeros('topographic__elevation', at='node')
z_hex += np.random.rand(z_hex.size)

raster_mg.set_watershed_boundary_condition_outlet_id(49, z_raster)
hex_mg.set_watershed_boundary_condition_outlet_id(24, z_hex)

k_sp1 = 1e-5
k_sp2 = 1e-6

K_sp_h = np.zeros(hex_mg.number_of_nodes)
K_sp_h[np.where(hex_mg.y_of_node <= 250)[0]]= k_sp1
K_sp_h[np.where(hex_mg.y_of_node > 250)[0]]=k_sp2

K_sp_r = np.zeros(raster_mg.number_of_nodes)
K_sp_r[np.where(raster_mg.y_of_node <= 250)[0]]= k_sp1
K_sp_r[np.where(raster_mg.y_of_node > 250)[0]]=k_sp2

Ur = np.ones(raster_mg.number_of_nodes)
Uh = np.ones(hex_mg.number_of_nodes)
uplift_rate = 0.00005
Ur = Ur*uplift_rate
Uh = Uh*uplift_rate

K_sp = 5E-6
dt = 1000
n_steps = 100001

uplift_per_step_r = dt * Ur
uplift_per_step_h = dt * Uh

fa_r = FlowAccumulator(raster_mg, flow_director="D8", depression_finder="DepressionFinderAndRouter")
sp_r = FastscapeEroder(raster_mg, K_sp=K_sp_r)

fa_h = FlowAccumulator(hex_mg, flow_director='Steepest',
                     depression_finder='DepressionFinderAndRouter')
sp_h = FastscapeEroder(hex_mg, K_sp=K_sp_h)

for i in range(n_steps):

    raster_mg.at_node['topographic__elevation'][raster_mg.core_nodes] += uplift_per_step_r[raster_mg.core_nodes]
    fa_r.run_one_step()
    sp_r.run_one_step(dt=dt)

    hex_mg.at_node['topographic__elevation'][hex_mg.core_nodes] += uplift_per_step_h[hex_mg.core_nodes]
    fa_h.run_one_step()
    sp_h.run_one_step(dt=dt)

    print(i)

    if i % 1000 == 0:
        fig, ((ax1, ax2)) = plt.subplots(1, 2, figsize=(12, 6))

        plt.sca(ax1)
        imshow_grid(raster_mg, 'topographic__elevation', cmap="terrain")
        ax1.set_title('Raster')

        plt.sca(ax2)
        imshow_grid(hex_mg, 'topographic__elevation',cmap="terrain")
        ax2.set_title('Hex')

        # Save the grid values to a text file
        txt_file_path = os.path.join(output_dir, 'raster_model_equi' + str(i) + 'years.txt')
        np.savetxt(txt_file_path, raster_mg.at_node['topographic__elevation'])

        txt_file_path = os.path.join(output_dir, 'hex_model_equi' + str(i) + 'years.txt')
        np.savetxt(txt_file_path, hex_mg.at_node['topographic__elevation'])

        # Save the plot to an image file
        img_file_path = os.path.join(output_dir, 'both_model_equi' + str(i) + 'years.png')
        plt.savefig(img_file_path)

        plt.close()

