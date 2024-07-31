import numpy as np

# Define the direction vectors
north_south_line = np.array([0, 1, 0])  # Along the y-axis
line_intersection = np.array([1, -1, 0])  # Line of intersection from the plane

# Calculate the dot product of the two vectors
dot_product = np.dot(north_south_line, line_intersection)

# Calculate the magnitudes (norms) of the vectors
magnitude_north_south = np.linalg.norm(north_south_line)
magnitude_line_intersection = np.linalg.norm(line_intersection)

# Calculate the cosine of the angle between the vectors
cos_theta = dot_product / (magnitude_north_south * magnitude_line_intersection)

# Calculate the angle in radians
angle_radians = np.arccos(cos_theta)

# Convert the angle to degrees
angle_degrees = np.degrees(angle_radians)

# Output the result
print(f"The angle between the north-south line and the line of the plane is {angle_degrees:.2f} degrees.")

# import numpy as np
#
#
# def plane_equation_with_angle(theta_deg, A=1):
#     """
#     Find a normal vector (A, B, C) for a plane that forms angle `theta` with the y-axis.
#     `theta_deg` is the angle in degrees.
#     `A` is an arbitrary choice for the normal vector's x-component.
#     """
#     # Convert theta from degrees to radians
#     theta_rad = np.radians(theta_deg)
#
#     # Calculate B using cos(theta) = B / sqrt(A^2 + B^2 + C^2)
#     # We choose an arbitrary A and solve for B and C (where C is arbitrarily chosen to be 1)
#     C = 1
#     A_squared = A ** 2
#     C_squared = C ** 2
#
#     # Calculate B
#     B = np.cos(theta_rad) * np.sqrt(A_squared + C_squared)
#
#     return A, B, C
#
#
# # Example usage
# theta_deg = 80  # Angle in degrees
# A, B, C = plane_equation_with_angle(theta_deg)
# print(f"The normal vector of the plane is: ({A}, {B}, {C})")

