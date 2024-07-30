##just a test change

import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from landlab import RasterModelGrid
from landlab.components import FlowAccumulator, FastscapeEroder
from landlab.plot import imshow_grid

output_dir = '/Users/poliveira/Library/CloudStorage/OneDrive-CityUniversityofNewYork/PhD_LIFE/PhD_2nd_Chapter/model_equi'  # Replace with your desired path

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

dx= 100
basin_mg = RasterModelGrid((250,250),dx)

basin_mg.set_closed_boundaries_at_grid_edges(True, True, False, True)

z = basin_mg.add_zeros('topographic__elevation', at='node')
z += np.random.rand(z.size)


U = np.ones(basin_mg.number_of_nodes)
uplift_rate = 0.00005
U = U*uplift_rate

K_sp = 5E-6
dt = 1000
n_steps = 100001

uplift_per_step = dt * U

fa = FlowAccumulator(basin_mg, flow_director="D8", depression_finder="DepressionFinderAndRouter")
sp = FastscapeEroder(basin_mg, K_sp=K_sp)

for i in range(n_steps):

    basin_mg.at_node['topographic__elevation'][basin_mg.core_nodes] += uplift_per_step[basin_mg.core_nodes]
    fa.run_one_step()
    sp.run_one_step(dt=dt)

    print(i)

    if i % 5000 == 0:

        imshow_grid(basin_mg, 'topographic__elevation')
        plt.title('Equi_Uplift ' + str(uplift_rate))

        # Save the grid values to a text file
        txt_file_path = os.path.join(output_dir, 'model_equi' + str(i) + 'years.txt')
        np.savetxt(txt_file_path, basin_mg.at_node['topographic__elevation'])

        # Save the plot to an image file
        img_file_path = os.path.join(output_dir, 'model_equi' + str(i) + 'years.png')
        plt.savefig(img_file_path)

        plt.close()

