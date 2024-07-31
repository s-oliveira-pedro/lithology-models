
def angle_between_plane_and_horizontal(A, B, C):
    """ Function to calculate the angle between the plane and the horizontal plane

     :parameters
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

A, B, C, D = 5, 0, 1, 0

angle = angle_between_plane_and_horizontal(A, B, C)
print(f"The angle between the plane and the horizontal plane is {angle:.2f} degrees")





