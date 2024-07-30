def visualize_plan(a,b,c,d):

    import numpy as np
    import plotly.graph_objs as go
    import plotly.io as pio

    # Set the renderer to open plots in the default web browser
    pio.renderers.default = 'browser'

    # Define the coefficients of the plane equation: ax + by + cz = d
    a, b, c, d = 2, 3, -1, 6

    # Define the range for x and y
    x_range = np.linspace(-10, 10, 100)
    y_range = np.linspace(-10, 10, 100)

    # Create a mesh grid for x and y values
    X, Y = np.meshgrid(x_range, y_range)

    # Calculate the corresponding z values using the plane equation
    Z = (d - a*X - b*Y) / c

    # Create a trace for the plane
    plane_trace = go.Surface(z=Z, x=X, y=Y, opacity=0.7)

    # Set up the layout
    layout = go.Layout(
        title="3D Plane",
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z'
        )
    )

    # Create the figure
    fig = go.Figure(data=[plane_trace], layout=layout)

    # Display the plot in the default web browser
    fig.show()
