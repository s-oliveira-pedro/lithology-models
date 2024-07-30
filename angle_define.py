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

def angle_between_plane_and_horizontal(A, B, C):
    """ Function to calculate the angle between the plane and the horizontal plane

     :parameter
     A - x coefficient
     B - y coefficient
     C - z coefficient
     D - independent coefficient

     :return
     angle - angle between the plane and an horizontal plane
    """
    import numpy as np

    normal_vector = np.array([A, B, C])

    horizontal_normal = np.array([0, 0, 1])

    dot_product = np.dot(normal_vector, horizontal_normal)

    mag_normal_vector = np.linalg.norm(normal_vector)
    mag_horizontal_normal = np.linalg.norm(horizontal_normal)

    cos_theta = dot_product / (mag_normal_vector * mag_horizontal_normal)

    theta_radians = np.arccos(cos_theta)

    theta_degrees = np.degrees(theta_radians)

    return theta_degrees

A, B, C, D = 0.1, 0, 1, 0  # You can replace these with your values

angle = angle_between_plane_and_horizontal(A, B, C)
print(f"The angle between the plane and the horizontal plane is {angle:.2f} degrees")

visualize_plan(A,B,C,D)

