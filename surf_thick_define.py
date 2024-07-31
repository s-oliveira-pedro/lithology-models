import math
def calculate_surface_exposure(thickness,angle):

    angle_rad = math.radians(angle)

    surf_thickness = thickness/(math.tan(angle_rad))

    print(math.sin(angle_rad))

    return surf_thickness

angle = 78
thickness = 10

surf_thick = calculate_surface_exposure(thickness,angle)

print(f"The surface thickness is: {surf_thick}")


