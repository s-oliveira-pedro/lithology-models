import math
def calculate_surface_exposure(thickness,angle):

    angle_rad = math.radians(angle)

    surf_thickness = thickness/math.tan(angle_rad)

    return surf_thickness

angle = 34.99
thickness = 500

surf_thick = calculate_surface_exposure(thickness,angle)

print(f"The surface thickness is: {surf_thick}")
