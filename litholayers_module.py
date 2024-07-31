import numpy as np
import math

class Litho_models:

    def __init__(self, x,y):
        self.x = x
        self.y = y

    def angle_between_plane_and_horizontal(self):
        """Function to calculate the angle between the plane and the horizontal plane

        :return: angle between the plane and the horizontal plane in degrees
        """
        normal_vector = np.array([self.x, self.y, 1])
        horizontal_normal = np.array([0, 0, 1])
        dot_product = np.dot(normal_vector, horizontal_normal)

        mag_normal_vector = np.linalg.norm(normal_vector)
        mag_horizontal_normal = np.linalg.norm(horizontal_normal)

        cos_theta = dot_product / (mag_normal_vector * mag_horizontal_normal)

        theta_radians = np.arccos(cos_theta)

        theta_degrees = np.degrees(theta_radians)

        self.theta_degrees = theta_degrees
        self.normal_vector = normal_vector

        print(f"The layer dip is {theta_degrees:.2f} degrees")


    def calculate_surface_exposure(self,thickness):

        self.thickness = thickness

        angle_rad = math.radians(self.theta_degrees)

        surf_thickness = thickness/(math.tan(angle_rad))

        print(f"The outcrop area is: {surf_thickness:.2f} meters at t=0")

    def strike_plane(self):
        north_south_line = np.array([0, 1, 0])  # Along the y-axis
        line_intersection = np.array(self.normal_vector)  # Line of intersection from the plane

        dot_product = np.dot(north_south_line, line_intersection)

        magnitude_north_south = np.linalg.norm(north_south_line)
        magnitude_line_intersection = np.linalg.norm(line_intersection)

        cos_theta = dot_product / (magnitude_north_south * magnitude_line_intersection)

        angle_radians = np.arccos(cos_theta)

        angle_degrees = np.degrees(angle_radians)

        print(f"The strike of the plane is {angle_degrees:.2f} degrees.")

