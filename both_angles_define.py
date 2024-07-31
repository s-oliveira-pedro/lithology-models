import numpy as np


def normal_vector_from_angles(theta_y_deg, theta_xy_deg):
    """
    Calculate the normal vector components A, B, C given angles with y-axis and x-y plane.
    theta_y_deg: Angle with the y-axis in degrees.
    theta_xy_deg: Angle with the x-y plane in degrees.
    """
    # Convert angles from degrees to radians
    theta_y_rad = np.radians(theta_y_deg)
    theta_xy_rad = np.radians(theta_xy_deg)

    # Calculate B and C based on the angles
    B = np.cos(theta_y_rad)
    C = np.sin(theta_xy_rad)

    # Calculate the squared magnitude of the normal vector in the x-y plane
    A_squared = 1 - B ** 2 - C ** 2

    # Ensure A_squared is not negative to avoid invalid square root
    if A_squared < 0:
        raise ValueError(f"Invalid angles: B^2 + C^2 > 1. Cannot compute A.")

    # Compute A
    A = np.sqrt(A_squared)

    return A, B, C


# Example usage
theta_y_deg = 30  # Angle with the y-axis in degrees
theta_xy_deg = 30  # Angle with the x-y plane in degrees
try:
    A, B, C = normal_vector_from_angles(theta_y_deg, theta_xy_deg)
    print(f"The normal vector of the plane is: A = {A:.2f}, B = {B:.2f}, C = {C:.2f}")
except ValueError as e:
    print(e)


