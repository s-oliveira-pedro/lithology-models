import tkinter as tk
import numpy as np
from landlab import RasterModelGrid
from landlab.plot import imshow_grid
import matplotlib.pyplot as plt
from landlab.components import FlowAccumulator, FastscapeEroder



# Define your function here
def create_raster_model(dx, x, y,n_steps):
    basin_mg = RasterModelGrid((x, y), dx)
    basin_mg.set_closed_boundaries_at_grid_edges(True, True, False, True)
    z = basin_mg.add_zeros('topographic__elevation', at='node')
    z += np.random.rand(z.size)

    U = np.ones(basin_mg.number_of_nodes)
    uplift_rate = 0.00005
    U = U * uplift_rate

    K_sp = 5E-6
    dt = 1000
    n_steps = n_steps

    uplift_per_step = dt * U

    fa = FlowAccumulator(basin_mg, flow_director="D8", depression_finder="DepressionFinderAndRouter")
    sp = FastscapeEroder(basin_mg, K_sp=K_sp)

    for i in range(n_steps):
        basin_mg.at_node['topographic__elevation'][basin_mg.core_nodes] += uplift_per_step[basin_mg.core_nodes]
        fa.run_one_step()
        sp.run_one_step(dt=dt)

    return basin_mg


# Function to handle the button click event
def on_button_click():
    try:
        # Get the input values
        dx = float(entry1.get())
        x = int(entry2.get())
        y = int(entry3.get())
        n_steps = int(entry4.get())

        # Create raster model
        basin_mg = create_raster_model(dx, x, y,n_steps)

        # Update the result label
        result_label.config(text=f"Dx: {dx}, x: {x}, y: {y}")

        # Display the grid
        plt.figure()
        imshow_grid(basin_mg, 'topographic__elevation')
        plt.show()
    except ValueError:
        result_label.config(text="Please enter valid numbers.")


# Set up the main application window
root = tk.Tk()
root.title("Creating Landscape Evolution Model")

frame = tk.Frame(root)
frame.pack(padx=100, pady=100)

# Input fields
entry1 = tk.Entry(frame)
entry1.pack()
entry1.insert(0, "Enter cell size")

entry2 = tk.Entry(frame)
entry2.pack()
entry2.insert(0, "Enter number of cols")

entry3 = tk.Entry(frame)
entry3.pack()
entry3.insert(0, "Enter number of rows")

entry4 = tk.Entry(frame)
entry4.pack()
entry4.insert(0, "Enter time step")


# Button to trigger the function
button = tk.Button(frame, text="Generate grid", command=on_button_click)
button.pack(pady=5)

# Label to display the result
result_label = tk.Label(frame)
result_label.pack(pady=5)

# Run the application
root.mainloop()

