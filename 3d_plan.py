
def visualize_plan(a,b,c,d):
    import numpy as np
    import plotly.graph_objs as go
    import plotly.io as pio

    # Set the renderer to open plots in the default web browser
    pio.renderers.default = 'browser'

    # Define the range for x and y
    x_range = np.linspace(-10, 10, 100)
    y_range = np.linspace(-10, 10, 100)

    # Create a mesh grid for x and y values
    X, Y = np.meshgrid(x_range, y_range)

    # Calculate the corresponding z values using the plane equation
    Z = (d - a * X - b * Y) / c

    # Create a trace for the plane
    plane_trace = go.Surface(z=Z, x=X, y=Y, opacity=0.7)

    # Set up the layout with customized axis labels and tick marks
    layout = go.Layout(
        title="3D Plane",
        scene=dict(
            xaxis=dict(
                title='X Axis',  # Label for the x-axis
                titlefont=dict(size=18, color='blue'),  # Font size and color for the x-axis label
                tickfont=dict(size=14, color='black'),  # Font size and color for the x-axis ticks
                range=[-10, 10],  # Set the range for the x-axis
                tickvals=np.arange(-10, 11, 2),  # Define the tick values
                ticktext=['-10', '-8', '-6', '-4', '-2', '0', '2', '4', '6', '8', '10']  # Custom tick text
            ),
            yaxis=dict(
                title='Y Axis',  # Label for the y-axis
                titlefont=dict(size=18, color='green'),  # Font size and color for the y-axis label
                tickfont=dict(size=14, color='black'),  # Font size and color for the y-axis ticks
                range=[-10, 10],  # Set the range for the y-axis
                tickvals=np.arange(-10, 11, 2),  # Define the tick values
                ticktext=['-10', '-8', '-6', '-4', '-2', '0', '2', '4', '6', '8', '10']  # Custom tick text
            ),
            zaxis=dict(
                title='Z Axis',  # Label for the z-axis
                titlefont=dict(size=18, color='red'),  # Font size and color for the z-axis label
                tickfont=dict(size=14, color='black'),  # Font size and color for the z-axis ticks
                range=[-10, 10],  # Set the range for the z-axis
                tickvals=np.arange(-10, 11, 2),  # Define the tick values
                ticktext=['-10', '-8', '-6', '-4', '-2', '0', '2', '4', '6', '8', '10']  # Custom tick text
            )
        )
    )

    # Create the figure
    fig = go.Figure(data=[plane_trace], layout=layout)

    # Display the plot in the default web browser
    fig.show()

a = 1
b = 0.24
c = 1
d = 0

visualize_plan(a,b,c,d)