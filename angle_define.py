import numpy as np


# Function to calculate the angle between the plane and the horizontal plane
def angle_between_plane_and_horizontal(A, B, C):
    # Normal vector of the plane
    normal_vector = np.array([A, B, C])

    # Normal vector of the horizontal plane (z-axis)
    horizontal_normal = np.array([0, 0, 1])

    # Dot product of the two normal vectors
    dot_product = np.dot(normal_vector, horizontal_normal)

    # Magnitudes of the normal vectors
    mag_normal_vector = np.linalg.norm(normal_vector)
    mag_horizontal_normal = np.linalg.norm(horizontal_normal)

    # Cosine of the angle
    cos_theta = dot_product / (mag_normal_vector * mag_horizontal_normal)

    # Angle in radians
    theta_radians = np.arccos(cos_theta)

    # Convert to degrees
    theta_degrees = np.degrees(theta_radians)

    return theta_degrees


# Example plane equation coefficients (A, B, C, D)
A, B, C, D = 0.7, 0.8, 1, 0  # You can replace these with your values

# Calculate the angle
angle = angle_between_plane_and_horizontal(A, B, C)
print(f"The angle between the plane and the horizontal plane is {angle:.2f} degrees")

